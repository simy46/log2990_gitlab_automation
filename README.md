# Section 8 - LOG2990 Correction

## 1. Create a token to use the API
https://gitlab.com/-/user_settings/personal_access_tokens?page=1&state=active&sort=expires_asc

![img](/assets/permissions.png)


copy token on `/utils/consts.py` to the variable `GITLAB_TOKEN`

you can now run with `python main.py` or `python 8_X.py` to run all the script or run each one separately. i suggest running each script one by one because it only prints the messagesé

**Note** : 
- 8_1 isn't complete as i cannot seem to fetch issues on issue board. have to do it manually
- 8_2 is not here as it cannot be scripted/ automated