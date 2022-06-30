# nofluff-scraper
nofluff-scraper

```yaml
## Usage:
python skills.py devops
python skills.py terraform

cat devops-skills.txt | jq '.[] .musthave [],[. [] | select( has("nice2have") == true )] [] .nice2have []' | sort | uniq -c | sort -n
cat devops-skills.txt | jq '.[] .musthave []' | sort | uniq -c | sort -n
cat devops-skills.txt | jq '[. [] | select( has("nice2have") == true )] [] .nice2have []' | sort | uniq -c | sort -n
cat python-skills.txt | jq ' map(select(.url | contains ("senior") | not ) | select(.url | contains ("fullstack") | not) ) | .[] ' | grep url

```