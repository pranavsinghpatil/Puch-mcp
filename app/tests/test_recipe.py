import requests

BASE_URL = "http://localhost:8000/get_recipe"
USER_ID = "test_user_1"

def test_query(query):
    resp = requests.get(BASE_URL, params={"user_id": USER_ID, "dish": query})
    print(f"Query: {query}\nResponse:\n{resp.json()['response']}\n{'-'*40}")

if __name__ == "__main__":
    test_query("biryani")       # should show guess or recipe
    # test_query("andhra style")             # select first option (if options given)
    test_query("2")     # show recommendations fully
    test_query("biriani")       # typo fuzzy test
    test_query("10")            # invalid option number test
