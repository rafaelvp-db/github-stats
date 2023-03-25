from github import Github
import os


def get_repos(github_user: str):

    access_token = os.environ["GITHUB_ACCESS_TOKEN"]
    g = Github(access_token)
    user = g.get_user(login="rafaelvp-db")
    repos = user.get_repos()

    return repos

def get_repo_statistics(
    repos,
    metrics = ["views", "clones"]
):
    
    result_views = []
    result_clones = []

    for repo in repos:
        if "views" in metrics:
            views = repo.get_views_traffic(per = "day")
            list_views = [
                {
                    "repo": repo.name,
                    "uniques": view.uniques,
                    "count": view.count,
                    "timestamp": view.timestamp
                }
                for view in views["views"]
            ]

        result_views.extend(list_views)

        if "clones" in metrics:
            clones = repo.get_clones_traffic(per = "day")
            list_clones = [
                {
                    "repo": repo.name,
                    "uniques": clone.uniques,
                    "count": clone.count,
                    "timestamp": clone.timestamp
                }
                for clone in clones["clones"]
            ]
    
        result_clones.extend(list_clones)

    return result_views, result_clones

def save_output(
        result_views = [],
        result_clones = [],
        output_path = "/tmp"
    ):
    if len(result_views) > 0:
        with open(f"{output_path}/views.json", "w") as file:
            file.write(str(result_views))
        with open(f"{output_path}/clones.json", "w") as file:
            file.write(str(result_clones))


if __name__ == "__main__":

    user_id = os.environ["GITHUB_USER_ID"]
    output_path = os.environ["OUTPUT_PATH"]

    repos = get_repos(user_id)
    view_stats, clone_stats = get_repo_statistics(repos = repos)
    save_output(
        result_views = view_stats,
        result_clones = clone_stats,
        output_path = output_path
    )