def main():
    import requests
    import xml.etree.ElementTree as ET

    # Define the query parameters
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": "all:electron",  # Search term
        "start": 0,
        "max_results": 1,
    }

    # Make the GET request to arXiv API
    response = requests.get(base_url, params=params)

    # Check for successful response
    if response.status_code == 200:
        # Parse the XML
        root = ET.fromstring(response.text)

        # Namespaces (arXiv uses Atom XML)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # Loop over each entry (paper)
        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            authors = [
                author.find("atom:name", ns).text
                for author in entry.findall("atom:author", ns)
            ]
            link = entry.find("atom:id", ns).text.strip()

            # Print the parsed info
            print("Title:", title)
            print("Summary:", summary)
            print("Authors:", ", ".join(authors))
            print("Link:", link)
    else:
        print(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    main()
