from prefect import task, flow
import requests


@flow(log_prints=True)
def get_repo_info():
    url = "https://api.github.com/repos/PrefectHQ/prefect"
    api_response = requests.get(url)
    if api_response.status_code == 200:
        repo_info = api_response.json()
        stars = repo_info["stargazers_count"]
        forks = repo_info["forks_count"]
        contributors_url = repo_info["contributors_url"]
        contributors = get_contributors(contributors_url)
        average_commits = calculate_average_commits(contributors)
        print(f"PrefectHQ/prefect repository statistics 🤓:")
        print(f"Stars 🌠 : {stars}")
        print(f"Forks 🍴 : {forks}")
        print(f"Average commits per contributor 💌 : {average_commits:.2f}")
    else:
        raise Exception("Failed to fetch repository information.")


@task()
def get_contributors(url):
    response = requests.get(url)
    if response.status_code == 200:
        contributors = response.json()
        return len(contributors)
    else:
        raise Exception("Failed to fetch contributors.")


@task()
def calculate_average_commits(contributors):
    commits_url = f"https://api.github.com/repos/PrefectHQ/prefect/stats/contributors"
    response = requests.get(commits_url)
    if response.status_code == 200:
        commit_data = response.json()
        total_commits = sum(c["total"] for c in commit_data)
        average_commits = total_commits / contributors
        return average_commits
    else:
        raise Exception("Failed to fetch commit information.")


# Run flow

if __name__ == "__main__":
    get_repo_info()
