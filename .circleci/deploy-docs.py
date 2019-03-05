import os
import sys
import subprocess as sp

git_username = "Grabl"
git_email = "grabl@grakn.ai"
grabl_credential = "grabl:"+os.environ['GRABL_CREDENTIAL']

web_dev_url = "github.com/graknlabs/web-dev.git"
update_branch = sys.argv[1]
web_dev_clone_location = os.path.join("web-dev")
docs_submodule_location = os.path.join(web_dev_clone_location, "docs")

commit_msg = "update docs submodule"

if __name__ == '__main__':
    try:
        print('This job will attempt to deploy the latest documentation to production')
        sp.check_output(["git", "config", "--global", "user.email", git_email])
        sp.check_output(["git", "config", "--global", "user.name", git_username])

        # --recursive clones web-dev as well as the docs submodule
        print('Cloning ' + web_dev_url + ' (' + update_branch + ' branch)')
        sp.check_output(["git", "clone", "--recursive", "https://"+grabl_credential+"@"+web_dev_url, web_dev_clone_location], stderr=sp.STDOUT) # redirect stderr to silence the output from git

        print('Checking out "' + update_branch + '"')
        sp.check_output(["git", "checkout", update_branch], cwd=web_dev_clone_location)

        print('Updating submodule at "' + docs_submodule_location + '"')
        sp.check_output(["git", "checkout", update_branch], cwd=docs_submodule_location)
        sp.check_output(["git", "pull", "origin", update_branch], cwd=docs_submodule_location)
        sp.check_output(["git", "add", "."], cwd=web_dev_clone_location)
        
        # the command returns 1 if there is a staged file. otherwise, it will return 0
        should_commit = sp.call(["git", "diff", "--staged", "--exit-code"], cwd=web_dev_clone_location) == 1
        
        if should_commit:
            print('Pushing(deploying) to '+update_branch)
            sp.check_output(["git", "commit", "-m", commit_msg], cwd=web_dev_clone_location)
            sp.check_output(["git", "push", "https://"+grabl_credential+"@"+web_dev_url, update_branch], cwd=web_dev_clone_location)
            print('Done!')
        else:
            print(web_dev_url + ' already contains the latest docs. There is nothing to deploy to production.')
    except sp.CalledProcessError as e:
        print('An error occurred when running "' + str(e.cmd) + '". Process exited with code ' + str(e.returncode) + ' and message "' + e.output + '"')
        raise e