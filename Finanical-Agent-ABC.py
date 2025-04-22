import json
import os
import openai

def get_api_key():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise EnvironmentError("Please set the OPENAI_API_KEY environment variable")
    return key

def get_valid_knowledge_level():
    level = input("Please choose your finance knowledge level by typing either 'advanced' or 'beginner': ")
    return level.strip().lower()

def generate_gpt_response_direct(level):
    markdown_reference = r'''
# h1 Heading
## h2 Heading
### h3 Heading
#### h4 Heading
##### h5 Heading
###### h6 Heading

Alternatively, for H1 and H2, an underline-ish style:

Alt-H1
======
Alt-H2
------

# Emphasis
Emphasis, aka italics, with *asterisks* or _underscores_.
Strong emphasis, aka bold, with **asterisks** or __underscores__.
Combined emphasis with **asterisks and _underscores_**.
Strikethrough uses two tildes. ~~Scratch this.~~
**This is bold text**
__This is bold text__
*This is italic text*
_This is italic text_
~~Strikethrough~~

# Lists
1. First ordered list item
2. Another item
   * Unordered sub-list.
1. Actual numbers don't matter, just that it's a number
   1. Ordered sub-list
4. And another item.

   You can have properly indented paragraphs within list items. Notice the blank line above, and the leading spaces.
   To have a line break without a paragraph, you will need to use two trailing spaces.  
   Note that this line is separate, but within the same paragraph.
   (This is contrary to the typical GFM line break behaviour.)

* Unordered list can use asterisks
- Or minuses
+ Or pluses

1. Make my changes
    1. Fix bug
    2. Improve formatting
        - Make the headings bigger
2. Push my commits to GitHub
3. Open a pull request
    * Describe my changes
    * Mention all the members of my team
        * Ask for feedback

+ Create a list by starting a line with +, -, or *
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Example sub-list item
    + Another sub-item
    - Another one
+ Very easy!

# Task lists
- [x] Finish my changes
- [ ] Push my commits to GitHub
- [ ] Open a pull request
- [x] @mentions, #refs, [links](), **formatting**, and <del>tags</del> supported
- [x] List syntax required (any unordered or ordered list supported)
- [ ] This is a complete item
- [ ] This is an incomplete item

# Ignoring Markdown formatting
You can escape Markdown formatting by using a backslash.
Let's rename \*our-new-project\* to \*our-old-project\*.

# Links
[I'm an inline-style link](https://www.google.com)
[I'm an inline-style link with title](https://www.google.com "Google's Homepage")
[I'm a reference-style link][Reference]
[I'm a relative reference to a repository file](../blob/master/LICENSE)
[You can use numbers for reference-style link definitions][1]
Or leave it empty and use the [link text itself].

[Reference]: https://www.mozilla.org  
[1]: http://slashdot.org  
[link text itself]: http://www.reddit.com

# Images
Here's our logo (hover to see the title text):

Inline-style:
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
Reference-style:
![alt text][logo]
[logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
![Minion](https://octodex.github.com/images/minion.png)
![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")

# [Footnotes](https://github.com/markdown-it/markdown-it-footnote)
Footnote 1 link[^first].
Footnote 2 link[^second].
Inline footnote^[Text of inline footnote] definition.
Duplicated footnote reference[^second].
[^first]: Footnote **can have markup** and multiple paragraphs.
[^second]: Footnote text.

Inline `code` has `back-ticks around` it.
'''
    
    query = input("Enter your financial query: ")
    lower_query = query.lower()
    
    topics = []
    if "income statement" in lower_query or "income" in lower_query:
        topics.append("Income Statement")
    if "balance sheet" in lower_query or "balance" in lower_query:
        topics.append("Balance Sheet")
    if "cash flow" in lower_query:
        topics.append("Cash Flow")
    
    if not topics:
        topics.append("General Financial Analysis")
    
    analysis_sections = ""
    for topic in topics:
        if topic == "Income Statement":
            analysis_sections += (
                "### Income Statement Analysis\n\n"
                "#### Revenue Trends:\n"
                "- Provide two long paragraphs: the first with detailed numerical data (e.g. YoY, QoQ growth, segmentation with references); "
                "the second with additional context and interpretation.\n\n"
                "#### Cost Structure and Margins:\n"
                "- Provide two long paragraphs: the first with concrete data on gross, operating, and net margins (with online research and references); "
                "the second with further context and interpretation.\n\n"
                "#### Earnings Performance:\n"
                "- Provide two long paragraphs: the first with detailed figures on net income, EPS, and comparisons with analyst estimates (with references); "
                "the second with additional context and interpretation.\n\n"
            )
        elif topic == "Balance Sheet":
            analysis_sections += (
                "### Balance Sheet Overview\n\n"
                "#### Asset Composition:\n"
                "- Provide two long paragraphs: the first with detailed figures on total assets and their breakdown (current vs. long-term) with references; "
                "the second with additional context and interpretation.\n\n"
                "#### Liabilities and Debt:\n"
                "- Provide two long paragraphs: the first with numerical data on liabilities (short-term vs. long-term) and debt-to-equity ratio (with references); "
                "the second with further context and interpretation.\n\n"
                "#### Equity Health:\n"
                "- Provide two long paragraphs: the first with detailed figures on shareholders' equity and book value per share (with references); "
                "the second with additional context and interpretation.\n\n"
            )
        elif topic == "Cash Flow":
            analysis_sections += (
                "### Cash Flow Insights\n\n"
                "#### Operating Cash Flow:\n"
                "- Provide two long paragraphs: the first with detailed numerical data on operating cash flow trends (with references); "
                "the second with further context and interpretation.\n\n"
                "#### Free Cash Flow (FCF):\n"
                "- Provide two long paragraphs: the first with detailed figures on FCF (cash after capital expenditures) with references; "
                "the second with additional context and interpretation.\n\n"
                "#### Cash Conversion:\n"
                "- Provide two long paragraphs: the first with numerical data on how quickly revenues convert into cash (with references); "
                "the second with further context and interpretation.\n\n"
            )
        else: 
            analysis_sections += (
                "### General Financial Analysis\n\n"
                "#### Analysis:\n"
                "- Provide two long paragraphs: the first with detailed numerical data and online references; "
                "the second with additional context and interpretation.\n\n"
            )
    
    if len(topics) == 1:
        head_title = f"**{topics[0]} Analysis for [Company] [Time Range]**"
    else:
        joined_topics = ", ".join(topics)
        head_title = f"**Financial Statements: Understanding [Company]'s {joined_topics} for [Time Range]**"
    
    if level == "beginner":
        language_instructions = (
            "Use simple, clear language and explain complex finance terms in easy words. "
            "For example, explain 'gross margin' as 'money left after direct costs'."
        )
    else:
        language_instructions = "Use detailed technical language with precise finance terminology."
    
    prompt_message = (
        "You are a financial expert. Based on the following financial query, generate a structured and analytical response in Markdown format. "
        "Only include analysis for the topics mentioned in the query.\n\n"
        "Language instructions: " + language_instructions + "\n\n"
        "Head Title:\n" + head_title + "\n\n"
        "Analysis Sections:\n\n" + analysis_sections + "\n\n"
        "Use the following Markdown style guidelines as reference:\n\n"
        + markdown_reference + "\n\n"
        "Answer the financial query with concrete analysis, including online research with references, rather than generic definitions.\n\n"
        "Financial Query: " + query
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant who provides detailed analysis with online research and references."},
            {"role": "user", "content": prompt_message}
        ],
        temperature=0.7,
    )
    return response.choices[0].message['content']

def main():
    level = get_valid_knowledge_level()
    print("Final classified finance knowledge level:", level)
    
    print("\n--- Generating ChatGPT Response ---\n")
    result = generate_gpt_response_direct(level)
    print(result)

if __name__ == "__main__":
    main()