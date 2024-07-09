// tag::imports[]
import com.vaticle.typedb.common.collection.Either;
import com.vaticle.typedb.common.concurrent.NamedThreadFactory;
import com.vaticle.typedb.driver.TypeDB;
import com.vaticle.typedb.driver.api.TypeDBCredential;
import com.vaticle.typedb.driver.api.TypeDBDriver;
import com.vaticle.typedb.driver.api.TypeDBSession;
import com.vaticle.typedb.driver.api.TypeDBTransaction;
import javax.lang.model.type.NullType;
import java.io.*;
import java.util.Iterator;
import java.util.List;
import java.util.Set;
import java.util.ArrayList;
import java.util.NoSuchElementException;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import static java.nio.charset.StandardCharsets.UTF_8;
// end::imports[]

// tag::class_query_iterator[]
public class QueryIterator implements Iterator<String> {
    public final List<String> filepaths;
    private Iterator<String> lineIterator;
    private boolean finished;

    public QueryIterator(ArrayList<String> filepaths) throws FileNotFoundException {
        this.filepaths = filepaths;
        finished = false;
        prepNextIterator();
    }

    private static InputStream inputStream(String filepath) throws FileNotFoundException {
        try {
            return new BufferedInputStream(new FileInputStream(filepath));
        } catch (IOException e) {
            throw new FileNotFoundException();
        }
    }

    private void prepNextIterator() throws FileNotFoundException {
        if (this.filepaths.isEmpty()) {
            finished = true;
        } else {
            InputStream inputStream = inputStream(filepaths.remove(0));
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, UTF_8));
            lineIterator = bufferedReader.lines().iterator();
            if (!lineIterator.hasNext()) prepNextIterator();
        }
    }

    @Override
    public boolean hasNext() {
        return !finished;
    }

    @Override
    public String next() {
        String nextItem = lineIterator.next();

        if (!lineIterator.hasNext()) {
            try {
                this.prepNextIterator();
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
        }

        return nextItem;
    }
}
// end::class_query_iterator[]

// tag::class_batch_iterator[]
public class BatchIterator implements Iterator<List<String>> {
    public int batchSize;
    private final Iterator<String> queries;

    public BatchIterator(ArrayList<String> filepaths, int batchSize) throws FileNotFoundException {
        this.batchSize = batchSize;
        this.queries = new QueryIterator(filepaths);
    }

    @Override
    public boolean hasNext() { return queries.hasNext(); }

    @Override
    public List<String> next() {
        if (!this.hasNext()) throw new NoSuchElementException();
        List<String> batch = new ArrayList<>();

        while (queries.hasNext() && batch.size() < batchSize) {
            batch.add(queries.next());
        }

        return batch;
    }
}
// end::class_batch_iterator[]

// tag::method_load_batch[]
public static void loadBatch(TypeDBSession session, List<String> batch) {
    try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
        for (String query: batch) {
            transaction.query().insert(query);
        }
        transaction.commit();
    }
}
// end::method_load_batch[]

// tag::method_load_data[]
public static void loadData(Set<String> addresses, String username, String password) throws FileNotFoundException {
    String database = "bookstore";
    ArrayList<String> dataFiles = new ArrayList<>(List.of("contributors.tql", "publishers.tql", "books.tql"));
    int batchSize = 100;
    TypeDBCredential credential = new TypeDBCredential(username, password, true);

    try (TypeDBDriver driver = TypeDB.cloudDriver(addresses, credential)) {
        try (TypeDBSession session = driver.session(database, TypeDBSession.Type.DATA)) {
            BatchIterator batchIterator = new BatchIterator(dataFiles, batchSize);

            while (batchIterator.hasNext()) {
                List<String> batch = batchIterator.next();
                loadBatch(session, batch);
            }
        }
    }
}
// end::method_load_data[]

// tag::method_schedule_batch_loader[]
public static CompletableFuture<Void> scheduleBatchLoader(
        ExecutorService executor,
        LinkedBlockingQueue<Either<List<String>, NullType>> queue,
        TypeDBSession session,
        AtomicBoolean hasError
) {
    return CompletableFuture.runAsync(() -> {
        Either<List<String>, NullType> queries;
        try {
            while ((queries = queue.take()).isFirst() && !hasError.get()) {
                try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
                    for (String query: queries.first()) {
                        transaction.query().insert(query);
                    }
                    transaction.commit();
                }
            }
        } catch (Throwable e) {
            hasError.set(true);
            throw new RuntimeException(e);
        }
    }, executor);
}
// end::method_schedule_batch_loader[]

// tag::method_load_data_async[]
public static void loadDataAsync(Set<String> addresses, String username, String password) throws InterruptedException, FileNotFoundException {
    String database = "bookstore";
    ArrayList<String> dataFiles = new ArrayList<>(List.of("contributors.tql", "publishers.tql", "books.tql"));
    int batchSize = 100;
    TypeDBCredential credential = new TypeDBCredential(username, password, true);

    try (TypeDBDriver driver = TypeDB.cloudDriver(addresses, credential)) {
        try (TypeDBSession session = driver.session(database, TypeDBSession.Type.DATA)) {
            for (String dataFile: dataFiles) {
                int poolSize = Runtime.getRuntime().availableProcessors();
                ExecutorService executor = Executors.newFixedThreadPool(poolSize, new NamedThreadFactory(database));
                LinkedBlockingQueue<Either<List<String>, NullType>> queue = new LinkedBlockingQueue<>(4 * poolSize);
                List<CompletableFuture<Void>> batchLoadersFutures = new ArrayList<>(poolSize);
                AtomicBoolean hasError = new AtomicBoolean(false);

                for (int i = 0; i < poolSize; i++) {
                    batchLoadersFutures.add(scheduleBatchLoader(executor, queue, session, hasError));
                }

                BatchIterator batchIterator = new BatchIterator(new ArrayList<>(List.of(dataFile)), batchSize);

                while (batchIterator.hasNext() && !hasError.get()) {
                    List<String> batch = batchIterator.next();
                    queue.put(Either.first(batch));
                }

                for (int i = 0; i < poolSize; i++) {
                    queue.put(Either.second(null));
                }

                CompletableFuture.allOf(batchLoadersFutures.toArray(new CompletableFuture[0])).join();
                executor.shutdown();
            }
        }
    }
}
// end::method_load_data_async[]
