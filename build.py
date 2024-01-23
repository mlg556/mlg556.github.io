import pathlib as plib
import subprocess as sbp
import frontmatter

from datetime import datetime


# build all .md files in posts to .html 
posts = plib.Path('.').glob("posts/**/*.md")
posts_metadata = []

for post in posts:
    # build
    fname = str(post)[:-3] # discard .md extension
    pandoc = ["pandoc", "-s", f"{fname}.md", "-t", "html5", "--katex", "--css", "style.css", "--highlight-style", "tango", "-A", "footer.html", "-H", "header.html", "-o", f"{fname}.html"]
    sbp.check_call(pandoc)
    # debug
    #print(" ".join(pandoc))

    # extract title, date as datetime object, and path of .html file
    # metadata = frontmatter.load(post)
    # date = datetime.strptime(metadata['date'], "%d %B %Y")
    # posts_metadata.append((metadata['title'], date, f"{fname}.html"))


# write index.md
    
# content = """
# # Posts

# """

# for p in posts_metadata:
#     content += f"- [{p[0]}]({p[2]})\n\n"

# content += "<!-- trick it into loading katex so i can use the fonts here as well. -->\n"
# content += "$\space$"

# with open("index.md", "w+") as f:
#     f.write(content)

# # build index.md to index.html
pandoc = ["pandoc", "-s", "index.md", "-t", "html5", "--katex", "--css", "style.css", "-A", "footer.html", "-H", "header.html", "-o", "index.html"]
sbp.check_call(pandoc)

