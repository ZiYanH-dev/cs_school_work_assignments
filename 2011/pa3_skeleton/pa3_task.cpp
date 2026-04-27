#include <cstring>

#include "constants.h"
#include "given.h"
#include "pa3_task.h"
#include "structures.h"

using namespace std;

/**
 * Task 1 - Register New User
 *
 * The `register_new_user` function registers a new user on the version control
 * system if no existing user has the specified username already.
 *
 * @param userManagement: reference to the `UserManagement` structure containing
 *                        the linked list of users.
 * @param username: the username of the new user to create.
 * @returns: `nullptr` if any validation failed; a pointer to the newly created
 *           user otherwise.
 */
const User *register_new_user(UserManagement &userManagement,
                              const char *username) {
  // TODO: Task 1
  return nullptr;
}

/**
 * Task 2 - Create Repository
 *
 * The `create_repository` function creates a repository with the specified name
 * under the specified owner, if no existing repository under the very user has
 * the same name as specified.
 *
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param owner: the owner of the new repository.
 * @param repoName: the name of the new repository.
 * @param creationTimestamp: the timestamp for the creation of the repository,
 *                           used for the initial commit.
 * @returns: -1 if any validation fails before repository creation; otherwise the
 *           index of the new repository in the `repos` array of the
 *           `RepositoryManagement` structure.
 */
int create_repository(RepositoryManagement &repoManagement, User *owner,
                      const char *repoName, const time_t creationTimestamp) {
  // TODO: Task 2
  return -1;
}

/**
 * Task 3 - Create Branch
 *
 * The `create_branch` function creates a branch in the specified repository
 * with the supplied name and creator of the branch, at the specified commit,
 * if no existing branch has the same name already.
 *
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param repoFQN: the fully-qualified name of the repository to create a branch
 *                 for.
 * @param branchName: the name of the branch to create.
 * @param creator: pointer to the creator user of the branch
 * @param commit: the commit to create the branch from.
 * @returns: false if any validation failed; true if the branch was created
 *           successfully.
 */
bool create_branch(RepositoryManagement &repoManagement, char *repoFQN,
                   const char *branchName, const User *creator,
                   const Commit *commit) {
  // TODO: Task 3
  return false;
}

/**
 * Task 4 - Add Commit
 *
 * The `add_commit` function adds a commit in the specified repository
 * with an optionally-specified branch to add the commit to. The hash
 * of the commit is computed from the author and message of the current
 * commit, as well as those of the previous commit (if any).
 *
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param author: the author of the commit.
 * @param repoFQN: fully-qualified name of the repository to add the commit
 *                 to.
 * @param commitMessage: the message of the commit.
 * @param branch: optionally, the branch the commit is added to.
 * @param timestamp: the timestamp when the commit was created.
 */
void add_commit(RepositoryManagement &repoManagement, const User *author,
                char *repoFQN, const char *branch, const char *commitMessage,
                time_t timestamp) {
  // TODO: Task 4
}

/**
 * Task 5 - Transfer Ownership
 *
 * The `transfer_ownership` function transfers the ownership of a repository
 * from its current owner to another user. Both users have to be registered
 * users on the platform.
 *
 * @param userManagement: reference to the `UserManagement` structure containing
 *                        the linked list of users.
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param fromUsername: the name of the current owner of the specified
 *                      repsitory.
 * @param toUsername: the new owner of the specified repository.
 * @param repoName: the name of the repository.
 * @returns: true if the ownership transfer was successful; false otherwise.
 */
bool transfer_ownership(UserManagement &userManagement,
                        RepositoryManagement &repoManagement,
                        const char *fromUsername, const char *toUsername,
                        const char *repoName) {
  // TODO: Task 5
  return false;
}

/**
 * Task 6 - Create Pull Request
 *
 * The `create_pull_request` function creates a pull request from one branch of
 * a repository to another. The repositories can be different.
 *
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param title: the creator of the pull request
 * @param author: the author of the pull request
 * @param fromBranchFQN: fully-qualified name of the branch to make a pul
 *                        request from.
 * @param toBranchFQN: fully-qualified name of the branch to merge the
 *                      suggested changes to.
 * @returns: true if the pull request was created successfully.
 */
bool create_pull_request(const RepositoryManagement &repoManagement,
                         const char *title, const User *author,
                         char *fromBranchFQN, char *toBranchFQN) {
  // TODO: Task 6
  return false;
}

/**
 * Task 7 - Fork Repository
 *
 * The `fork_repository` function allows the creation of forks of repositories.
 *
 * @param userManagement: reference to the `UserManagement` structure containing
 *                        the linked list of users.
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param owner: the owner of the repository to create the fork from.
 * @param forkedOwner: the ownr of the forked repository.
 * @param repoToFork: the name of the repository to fork.
 * @returns true if the repository was forked successfully; false otherwise.
 */
bool fork_repository(UserManagement &userManagement,
                     RepositoryManagement &repoManagement, const User *owner,
                     const char *forkedOwner, const char *repoToFork) {
  // TODO: Task 7
  return false;
}

/**
 * Task 8.1 - Merge Pull Request (Squash Merge)
 *
 * The `merge_pull_request_squashmerge` function merges the specified
 * pull request in a repsitory using the squash merge strategy
 * (combines all commits in the pull request into one and add it to the target
 * branch).
 *
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param repoFQN: the name of the repository to merge a pull request for.
 * @param prNumber: the number of the pull request to merge.
 * @param timestamp: the timestamp when this pull request was merged.
 */
void merge_pull_request_squashmerge(RepositoryManagement &repoManagement,
                                    char *repoFQN, int prNumber,
                                    time_t timestamp) {
  // TODO: Task 8.1
}

/**
 * Task 8.2 - Merge Pull Request (Rebase Merge)
 *
 * The `merge_pull_request_rebasemerge` function merges the specified
 * pull request in a repsitory using the rebase merge strategy
 * (rebases all commits in the pull request to the target branch).
 *
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param repoFQN: the name of the repository to merge a pull request for.
 * @param prNumber: the number of the pull request to merge.
 * @param timestamp: the timestamp when this pull request was merged.
 */
void merge_pull_request_rebasemerge(RepositoryManagement &repoManagement,
                                    char *repoFQN, int prNumber,
                                    time_t timestamp) {
  // TODO: Task 8.2
}

/**
 * Task 8.3 - Merge Pull Request (Merge Commit)
 *
 * The `merge_pull_request_mergecommit` function merges the specified
 * pull request in a repsitory using the merge commit strategy
 * (adds all commits to the target branch preserving chronological order, with a
 * final merge commit added).
 *
 * This is slightly different from what actually happens when a merge commit
 * is used, but for simplicity's sake this is done instead.
 *
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositories.
 * @param repoFQN: the name of the repository to merge a pull request for.
 * @param prNumber: the number of the pull request to merge.
 * @param timestamp: the timestamp when this pull request was merged.
 */
void merge_pull_request_mergecommit(RepositoryManagement &repoManagement,
                                    char *repoFQN, int prNumber,
                                    time_t timestamp) {
  // TODO: Task 8.3
}

/**
 * Task 9 - De-register User
 *
 * The `deregister_user` function de-registers a user from the version control
 * system and updates any references to it with the ghost user. This deletes all
 * their repositories and then deallocates memory allocated to this user.
 *
 * @param userManagement: reference to the `UserManagement` structure containing
 *                        the linked list of users.
 * @param repoManagement: reference to the `RepositoryManagement` structure
 *                        containing the dynamic array of pointers to
 *                        repositopries.
 * @param username: the name of the user to de-register.
 */
void deregister_user(UserManagement &userManagement,
                     RepositoryManagement &repoManagement,
                     const char *username) {
  // TODO: Task 9
}
