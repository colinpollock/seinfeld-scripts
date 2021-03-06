#!/usr/bin/env python


import re
import sys



def unescape(s):
    """Replace HTML jibberish with normal symbols."""
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&#145;", "'")
    s = s.replace("&#146;", "'")
    s = s.replace("&#147;", "'")
    s = s.replace("&#148;", "'")
    s = s.replace("&#149;", "'")
    s = s.replace("&#150;", "'")

    s = s.replace("&quot;", "'")
    s = s.replace("&#133;", "...")


    # this has to be last:
    s = s.replace("&amp;", "&")
    return s


def remove_tags(text):
    """Returns the text with HTML tags removed."""
    return re.sub(r'<.*?>', '', text)


def parse_episode_info(html):
    """Return a dict with meta-info about the episode."""
    groups = re.search(r'pc: .*? season (\d+), episode (\d+)', html).groups()
    season_num = int(groups[0])
    episode_num = int(groups[1])

    title = re.search(r'Episode \d+(.*?) - (.*?)<', html).groups()[1]
    date = re.search(r'Broadcast date: (.*?)<', html).groups()[0]
    writers = re.search(r'Written [bB]y:? (.*?)<', html).groups()[0]
    writers = tuple([w.strip() for w in re.split(r',|&amp;', writers) if w])
    director = re.search(r'Directed [bB]y (.*?)<', html).groups()[0]

    return {'season_num': season_num, 'episode_num': episode_num, 
            'title': title, 'date': date, 'writers': writers, 
            'director': director}


def parse_script(html):
    """Returns a sequence of (speaker, utterance) pairs."""
    utterances = re.findall(r'([A-Z]+)(?: \(.*?\))?: (.*?)</?(?:br|p)>', html)

    for i, (speaker, utterance_text) in enumerate(utterances):
        # Skip the monologues at the beginning of episodes.
        if speaker.upper() == 'JERRY' and \
              i == 0 and \
              len(utterance_text.split()) > 100:
            continue

        yield (speaker, unescape(utterance_text))



def scrape_episode(html):
    html = html.replace('&nbsp;', ' ')
    splitted = re.split(r'={30}.*', html)
    info_html = splitted[0]
    script_html = splitted[1]
    info = parse_episode_info(info_html)

    utterances = parse_script(script_html)
    return (info, utterances)
