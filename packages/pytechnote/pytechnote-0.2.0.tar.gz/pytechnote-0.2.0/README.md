# TechNote

TechNote is a self-hosted, Markdown-based note-taking app which allows users to navigate, search and modify their Markdown files all in one place. It uses pandoc for parsing the Markdown files and offers a clean and responsive web-based user interface.

TechNote is designed to display each Markdown note as a standard HTML page for web browsers. On each page, there are options to access a table of contents and a list of the notes alongside a search box tool. These kind of tools allow users to navigate between notes and the headings of the notes in an easy and quick way. We are planing to add more features, but we are also considering to keep TehcNote, a distraction-free reading and writing environment.

#### Video Demo: https://www.youtube.com/watch?v=UcrlFcX5g8k

![TechNote](./static/docs/technote_01.png)
![TechNote](/static/docs/technote_01.png)

## Setting up

1. Open your terminal and clone the repository:

```shell
git clone https://github.com/miladnia/technote.git
```

2. `cd` to the root directory of TechNote.

3. If you have installed [`make`][make] just execute `make all` otherwise:

```shell
pip3 install -r requirements.txt
python3 init_db.py
```

> Notice: `pip` will install the `pypandoc_binary` package which includes pandoc out of the box. If pandoc is already installed (i.e. pandoc is in the `PATH`), pypandoc uses the version with the higher version number, and if both are the same, the already installed version. If you want to install pandoc yourself or are on a unsupported platform, you'll need to replace `pypandoc_binary` with `pypandoc` inside the `requirements.txt` file and [install pandoc manually][pandoc_install].

4. Run the HTTP serve using `make run` or:

```shell
python3 app.py
```

> Notice: The server will be run on port `8087`. Use `flask run --host=0.0.0.0 --port=<PORT_NUMBER>` to change the port number.

> Note: To run the app in debug mode use `make dev` or `flask run --debug` which will be run on port `5000`.

5. Open a browser and go to <http://127.0.0.1:8087> or <http://127.0.0.1:5000> if you have ran the `flask` command manually.

![the welcome page](./static/docs/welcome_page.png)
![the welcome page](/static/docs/welcome_page.png)

This is the welcome page that asking you to select the directories.

You might already have a single directory that contains some Markdown (`.md`) files, as I have one. Maybe that's the only directory you should choose. Otherwise, just select an arbitary directory to store new notes.

Don't touch anything, if you just want to try the app out. There are two default directories `examples/tech_notes` and `examples/personal_notes` which contain some example Markdown notes. They are selected already, just click the **Add notes** button to add the notes.

> Notice: The first directory you choose, is the place for new notes.

> Tip: You can begin a fresh start by running the `make fresh` command at any time. Notice the original Markdown files will be remain untouched.

## How it works

We are trying to keep everything as explicit as possible. TechNote just renders your Markdown files and show them as an HTML document. It does not modify your files automatically and it does not create files or directories inside your own directories.

Markdown is a plain text markup format created by John Gruber. For more information about Markdown, please visit John Gruber’s website at <http://www.daringfireball.net>.

TechNote stores cached versions of rendered Markdown files to avoid re-rendering them every time they are accessed and optimize performance. The cache is invalidated when the Markdown file is updated. When you access a note on TechNote, it checks if the cache is invalidated and then it re-render a new HTML document and updates the cache. The cache files are stored in the `.cache` directory which placed inside the root directory of the project.

TechNote uses a single SQLite database to only store some paths to directories and some meta data like a unique ID and a pretty name for each note which simply could be regenerated at any time. If you delete the database manually or using `make clean`, you will not loose anything important about the notes but you will loose the paths to the directories you have selected.

Use `make fresh` to remove the `.cache` directory and regenerate a fresh `notes.db` database file.

## Built With

- [Flask][flask] — Our back end is a Flask app written in Python.
- [Bootstrap][bootstrap] — Our responsive frond end is based on Bootstrap.
- [SQLite][sqlite] — Our data store is just a single file thanks to SQLite.
- [Pandoc][pandoc] — We use pandoc for parsing the Markdown files.
- [Pypandoc][pypandoc] — We use pypandoc as a wrapper for pandoc in Python.

## Creators

Milad Abdollahnia

- <https://github.com/miladnia>
- <https://twitter.com/xmiladnia>

## Copyright and license

TechNote is an open-source project licensed under the [MIT license][mit]. For the full copyright and license information, please read the [LICENSE](./LICENSE) file that was distributed with this source code.

[mit]: https://opensource.org/licenses/MIT
[flask]: https://github.com/pallets/flask
[pandoc]: https://github.com/jgm/pandoc
[pypandoc]: https://github.com/JessicaTegner/pypandoc
[pandoc_install]: https://pypi.org/project/pypandoc/#Installing-pandoc
[sqlite]: https://github.com/sqlite/sqlite
[bootstrap]: https://github.com/twbs/bootstrap/
[make]: https://www.gnu.org/software/make/
