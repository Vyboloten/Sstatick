from src.blocktype import markdown_to_html_node
from pathlib import Path
import os, shutil, urllib.request
print("Current working directory:", os.getcwd())

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")
    raise Exception ("No Header")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read the markdown file
    with open(from_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    # Read the template file
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    # Extract title from markdown
    title = extract_title(markdown_content)
    # Replace placeholders in template
    result_html = template_content.replace("{{ Title }}", title)
    result_html = result_html.replace("{{ Content }}", html_content)
    result_html = result_html.replace('href="/',f'href="{basepath}')
    result_html = result_html.replace('src="/', f'src="{basepath}')
    #dest_path = "public/blog/post.html"
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as html_file:
        html_file.write(result_html)

def create_index_md():
    # Ensure 'content' directory exists
    os.makedirs('content', exist_ok=True)

    # Define Markdown content
    markdown_content = """
# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev).
"""

    # Write the Markdown content to 'content/index.md'
    with open('content/index.md', 'w') as file:
        file.write(markdown_content)

def create_markdown_files():
    glorfindel_content = """# Why Glorfindel is More Impressive than Legolas

[< Back Home](/)

![Glorfindel image](/images/glorfindel.png)

> "The deeds of Glorfindel shine bright as the morning sun, whilst the feats of others are as the flickering of stars in the night sky."

In J.R.R. Tolkien's legendarium, characterized by its rich tapestry of noble heroes and epic deeds, two Elven luminaries stand out: **Glorfindel**, the stalwart warrior returned from the Halls of Mandos, and **Legolas**, the prince of the Woodland Realm. While both possess grace and valor beyond mortal ken, it is Glorfindel who emerges as the more compelling figure, a beacon of heroism whose legacy spans ages.

## Introduction

With my many years as an **Archmage**, delving into ancient tomes and consulting the wisdom of the stars, I have come to appreciate the dazzling tapestry of Middle-earth and its storied inhabitants. Among them, Glorfindel stands resplendent, his narrative a testament to resilience and might. As we unravel the threads of his tale, let us explore the reasons why this Elf-lord is more impressive than his Woodland counterpart.

## A Hero of Great Renown

### The Battle with the Balrog

While Legolas is famed for his prowess with a bow and his agility upon the battlefield, it is Glorfindel who etched his name into the annals of history with his legendary battle against a Balrog of Morgoth—an encounter both fearsome and fateful:

1. **A Noble Sacrifice**: In the ancient tales of Gondolin, it was Glorfindel who faced off against the fiery terror during the city's fall, sacrificing himself to secure his people's escape.
2. **A Victory Remembered**: Even in death, his victory was marked by valor, as he vanquished the Balrog in an epic struggle, ultimately earning a place of honor in the Undying Lands.

## A Beacon of Power and Wisdom

### Return from the Undying Lands

Unlike Legolas, whose journey begins in the Third Age, Glorfindel's saga spans millennia, demonstrating his integral role in the grand design of the Eldar and Valar:

- **The Gift of Rebirth**: Glorfindel's return to Middle-earth after his heroic demise is a profound testament to his worth, as the Valar saw fit to restore him to life, laden with greater wisdom and power.
- **The Role of a Guide**: Serving as an advisor and protector in Rivendell, his presence provided not only counsel but a formidable bulwark against dark forces.

```
print("Glorfindel")
print("the")
print("Balrog-Slayer")
```

## The Essence of Elven Might

### A Paragon of Strength

While Legolas enchants with his feats, Glorfindel embodies the quintessential strength and dignity of the Eldar, a figure whose very presence commands respect:

- **Elven Majesty**: Renowned for his radiant aura and golden hair, Glorfindel is described as exuding an aura of light akin to the Valar, a stark contrast to the stealthy, sylvan skill of Thranduil's son.
- **Fearless Leadership**: His leadership during times of strife underscores a dedication to duty and an unwavering resolve—a guiding light for both Elves and Men.

## Themes of **Enduring** Legacy

### An Impact on the Ages

Though Legolas's deeds are celebrated, Glorfindel's influence is woven directly into the vast narrative of Middle-earth—a bridge connecting its ancient past to its perilous future:

- **A Historical Touchstone**: His legacy casts long shadows over pivotal events, reinforcing the enduring themes of sacrifice and rebirth that resonate throughout the legendarium.
- **A Luminary of Legend**: Respected and revered in songs, his tale remains an inspiration, an immortal testament to courage—a rarity that transcends time.

## Conclusion

As we traverse the storied paths of Middle-earth, it becomes clear that while Legolas presents an appealing portrait of Elven grace, it is Glorfindel who embodies the very essence of heroism in Tolkien's world. His narrative transcends the ages, shining with a brilliance that stands unchallenged by the temporal feats of his peers. As an Archmage who has walked the hallowed halls of history, I assert with unyielding certainty that Glorfindel, the eternal light in the shadowed lands of legend, stands as the more impressive. His story, unparalleled and majestic, continues to inspire those who venture into the realms of fantasy and dare to dream of a time when such heroes strode the Earth.

Thus, in the grand council of Middle-earth's champions, let us recognize Glorfindel as a paragon whose legacy remains untarnished—a testament to the timeless grandeur of Tolkien's creation.
"""
    tom_content = """# Why Tom Bombadil Was a Mistake

[< Back Home](/)

![Tom Bombadil image](/images/tom.png)

> "Old Tom Bombadil is a merry fellow; bright blue his jacket is, and his boots are yellow. Alas, his merry song may not belong in this plot's prolonged confluence."

In the vast and intricate weave of J.R.R. Tolkien's legendarium, amidst heroes of renown and tales of high adventure, there exists a curious anomaly: Tom Bombadil. This peculiar figure, whimsical and unfettered by the weight of Middle-earth's burdens, has long been a point of contention among scholars and enthusiasts. While his character exudes charm and mystery, I, as an ancient **Archmage**, must assert that his inclusion in _The Lord of the Rings_ was, unfortunately, a narrative misstep.

_An unpopular opinion, I know._

## Introduction

Having traversed the corridors of Tolkien's sprawling world, immersed in its lore, I have come to understand the impact of cohesion and momentum in storytelling. Thus, I find myself compelled to examine Tom Bombadil's role and question the necessity of his presence within the epic saga. As we embark on this critical inquiry, let us consider the reasons why Old Tom's playful presence may be seen as a disruptive force.

## An Intriguing Yet Disjointed Figure

### A Divergence from Narrative Flow

Tolkien's epic is known for its meticulous pacing and the gravity of its themes. Enter Tom Bombadil—a character whose frivolity and detachment from worldly events create a jarring contrast within the otherwise cohesive narrative:

1. **An Unnecessary Interlude**: The encounter with Tom, while quaint and endearing, serves as a temporal diversion that detracts from the urgency of the Fellowship's quest.
2. **An Outlier in Purpose**: His escapades, while rich in mirth, add little to the central narrative, raising questions about their relevance in the grand design of Middle-earth.

## An Enigma that Remains Unresolved

### A Break from Coherence

In a tale defined by intricate connections and deeply rooted mythology, Bombadil's inexplicable nature poses a challenge to the narrative's internal logic:

- **A Mystery Without Resolution**: Unlike other enigmatic figures whose backstories enrich the tapestry, Tom remains enigmatic, shrouded in mystery that neither advances the plot nor deepens the lore.
- **A Departure from Tone**: His presence, filled with lighthearted songs and whimsical antics, contrasts sharply with the solemnity and tension that define the rest of the saga.

```
print("Tom")
print("Bombadil")
print("A")
print("Mystery")
```

## A Theme of **Disruption**

### An Element of Distraction

Tom Bombadil's inclusion inadvertently shifts focus from the pressing matters of Middle-earth, introducing themes that sit uneasily with the narrative's core:

- **A Shift in Focus**: His carefree demeanor and ability to withhold the power of the One Ring, while intriguing, distract from the overarching themes of sacrifice and moral complexity.
- **A Misstep in Continuity**: His segment, charming as it may be, disrupts the journey's continuous build-up towards the looming confrontation with darkness.

## Conclusion

As we ponder the manifold wonders and intricacies of Tolkien's world, it is evident that Tom Bombadil, while delightfully unique, was a narrative anomaly—a whimsical reflection in the mirror of Middle-earth's grand narrative. While his character captivates with a certain mystique, it answers questions that were never asked, leaving readers with more enigmas than revelations.

In conclusion, as one who has explored the mythic past of Middle-earth and sought coherence in its storied legacy, I propose that Tom Bombadil, for all his merriment and enigma, was a divergence from the tale's destined path—a curiosity that, while endearing to some, stands as a reminder that even in the most meticulously crafted worlds, not all paths lead to the fulfillment of the quest.

Thus, let us bid farewell to Old Tom with a final song, recognizing both his charm and the discord his presence sowed. For within the hallowed pages of Tolkien's masterpiece, every beat must resonate with purpose, lest the harmony of the tale be lost to idle whimsy.
"""
    majesty_content = """# The Unparalleled Majesty of "The Lord of the Rings"

[< Back Home](/)

![LOTR image artistmonkeys](/images/rivendell.png)

> "I cordially dislike allegory in all its manifestations, and always have done so since I grew old and wary enough to detect its presence.
> I much prefer history, true or feigned, with its varied applicability to the thought and experience of readers.
> I think that many confuse 'applicability' with 'allegory'; but the one resides in the freedom of the reader, and the other in the purposed domination of the author."

In the annals of fantasy literature and the broader realm of creative world-building, few sagas can rival the intricate tapestry woven by J.R.R. Tolkien in _The Lord of the Rings_. You can find the [wiki here](https://lotr.fandom.com/wiki/Legendarium).

## Introduction

This series, a cornerstone of what I, in my many years as an **Archmage**, have come to recognize as the pinnacle of imaginative creation, stands unrivaled in its depth, complexity, and the sheer scope of its _legendarium_. As we embark on this exploration, let us delve into the reasons why this monumental work is celebrated as the finest in the world.

## A Rich Tapestry of Lore

One cannot simply discuss _The Lord of the Rings_ without acknowledging the bedrock upon which it stands: **The Silmarillion**. This compendium of mythopoeic tales sets the stage for Middle-earth's history, from the creation myth of Eä to the epic sagas of the Elder Days. It is a testament to Tolkien's unparalleled skill as a linguist and myth-maker, crafting:

1. An elaborate pantheon of deities (the `Valar` and `Maiar`)
2. The tragic saga of the Noldor Elves
3. The rise and fall of great kingdoms such as Gondolin and Númenor

```
print("Lord")
print("of")
print("the")
print("Rings")
```

## The Art of **World-Building**

### Crafting Middle-earth

Tolkien's Middle-earth is a realm of breathtaking diversity and realism, brought to life by his meticulous attention to detail. This world is characterized by:

- **Diverse Cultures and Languages**: Each race, from the noble Elves to the sturdy Dwarves, is endowed with its own rich history, customs, and language. Tolkien, leveraging his expertise in philology, constructed languages such as Quenya and Sindarin, each with its own grammar and lexicon.
- **Geographical Realism**: The landscape of Middle-earth, from the Shire's pastoral hills to the shadowy depths of Mordor, is depicted with such vividness that it feels as tangible as our own world.
- **Historical Depth**: The legendarium is imbued with a sense of history, with ruins, artifacts, and lore that hint at bygone eras, giving the world a lived-in, authentic feel.

## Themes of _Timeless_ Relevance

### The _Struggle_ of Good vs. Evil

At its heart, _The Lord of the Rings_ is a timeless narrative of the perennial struggle between light and darkness, a theme that resonates deeply with the human experience. The saga explores:

- The resilience of the human (and hobbit) spirit in the face of overwhelming odds
- The corrupting influence of power, epitomized by the One Ring
- The importance of friendship, loyalty, and sacrifice

These universal themes lend the series a profound philosophical depth, making it a beacon of wisdom and insight for generations of readers.

## A Legacy **Unmatched**

### The Influence on Modern Fantasy

The shadow that _The Lord of the Rings_ casts over the fantasy genre is both vast and deep, having inspired countless authors, artists, and filmmakers. Its legacy is evident in:

- The archetypal "hero's journey" that has become a staple of fantasy narratives
- The trope of the "fellowship," a diverse group banding together to face a common foe
- The concept of a richly detailed fantasy world, which has become a benchmark for the genre

## Conclusion

As we stand at the threshold of this mystical realm, it is clear that _The Lord of the Rings_ is not merely a series but a gateway to a world that continues to enchant and inspire. It is a beacon of imagination, a wellspring of wisdom, and a testament to the power of myth. In the grand tapestry of fantasy literature, Tolkien's masterpiece is the gleaming jewel in the crown, unmatched in its majesty and enduring in its legacy. As an Archmage who has traversed the myriad realms of magic and lore, I declare with utmost conviction: _The Lord of the Rings_ reigns supreme as the greatest legendarium our world has ever known.

Splendid! Then we have an accord: in the realm of fantasy and beyond, Tolkien's creation is unparalleled, a treasure trove of wisdom, wonder, and the indomitable spirit of adventure that dwells within us all.
"""
    contact_content = """# Contact the Author

[< Back Home](/)

Give me a call anytime to chat about Tolkien!

`555-555-5555`

**"Váya márië."**"
"""
    # Now create a function that uses these variables
    # Create directories
    dirs = [
        'content/blog/glorfindel',
        'content/blog/tom',
        'content/blog/majesty',
        'content/contact'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    # Map file paths to their content
    content_mapping = {
        'content/blog/glorfindel/index.md': glorfindel_content,
        'content/blog/tom/index.md': tom_content,
        'content/blog/majesty/index.md': majesty_content,
        'content/contact/index.md': contact_content
    }
    
    # Write each file
    for file_path, content in content_mapping.items():
        with open(file_path, 'w') as file:
            file.write(content)

def copy_images():
    print("Starting to copy images...")
    # Ensure the destination directory exists
    os.makedirs('static/images', exist_ok=True)
    
    # Define URLs and corresponding local filenames
    image_urls = {
        'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/Q6J8StV.png': 'glorfindel.png',
        'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/HofqCKA.png': 'tom.png',
        'https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/DfGgjbd.png': 'rivendell.png'
    }
    
    # Download each image
    for url, filename in image_urls.items():
        print(f"Downloading {url} to static/images/{filename}...")
        try:
            # Use urllib to download the image
            filepath = f'static/images/{filename}'
            urllib.request.urlretrieve(url, filepath)
            print(f"Successfully downloaded {filename}")
            
            # Verify file exists and has content
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                print(f"Verified: {filepath} exists and has content")
            else:
                print(f"Warning: {filepath} doesn't exist or is empty")
                
        except Exception as e:
            print(f"Failed to download {url}: {e}")
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    """print(f"Processing directory: {dir_path_content}")
    #dir_path_content = 'content' just for understanding
    # Get all entries in the current directory
    entries = os.listdir(dir_path_content)
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        print(f"Found entry: {entry_path}")
        if os.path.isfile(entry_path) and entry.endswith('.md'):
            # 1. Get the markdown content
            with open(entry_path, 'r') as f:
                markdown_content = f.read()
            # 2. Convert to HTML
            html_node = markdown_to_html_node(markdown_content)
            html_content = html_node.to_html()
            # 3. Apply template
            with open(template_path, 'r') as f:
                template_content = f.read()
            final_html = template_content.replace('{{ Content }}', html_content)
            # 4. Write to destination (with .html extension instead of .md)
            rel_path = os.path.relpath(entry_path, 'content')
            dest_file_path = os.path.join(dest_dir_path, rel_path.replace('.md', '.html'))
            # Make sure the destination directory exists
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
            # Write the HTML file
            with open(dest_file_path, 'w') as f:
                f.write(final_html)
                print(f"Generated HTML file: {dest_file_path}")
        elif os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, dest_dir_path)"""
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)

def copy_static(source_dir, dest_dir):
# Ensure destination directory exists (create all necessary dirs)
    os.makedirs(dest_dir, exist_ok=True)
    # Get list of all items in source directory
    dir_list = os.listdir(source_dir)
    for item in dir_list:
        # Create full source path
        source_path = os.path.join(source_dir, item)
        # Create corresponding destination path
        dest_path = os.path.join(dest_dir, item)
        # Now you can use source_path and dest_path for your operations
        if os.path.isfile(source_path):
            # It's a file, copy it
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} to {dest_path}")
        elif os.path.isdir(source_path):
            # If it's a directory, create it in the destination as necessary
            # and recursively copy its contents
            os.makedirs(dest_path, exist_ok=True)
            print(f"Created directory: {dest_path}")
            copy_static(source_path, dest_path)  # Recursive call

def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)