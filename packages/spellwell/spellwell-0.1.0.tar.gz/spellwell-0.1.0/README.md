# SpellWell

`SpellWell` is a CLI application which allows you to practice spelling using your own wordlist.

The workflow is as follows:

1. While working on something and you're unsure of the spelling of a word, you can add it to your wordlist.
2. You type out the looked up word yourself in your desired text editor.
3. After you've reached a few words, you can start practicing spelling them.
4. Add them to the ~/.spellwell file and run the application.

## Installation

Install SpellWell directly from PyPI:

```bash
pip install spellwell
```

Or install the latest development version from GitHub:

```bash
pip install git+https://github.com/yourusername/SpellWell.git
```

After installation, you can use the `spellwell` command directly from your terminal.

## Features

- [x] Add words to your own wordlist with optional example sentences
- [x] Randomize the words for the user
- [x] Store the users results locally
- [x] Mode: "Guess the word" - Asks the user to complete blurred out word
- [x] Mode: "Use in sentence" - Shows example sentence with word blanked out
- [x] Command: "add" - Add words to the wordlist
- [x] Command: "list" - Show words from the wordlist
- [x] Command: "practice" - Practice spelling your words
- [x] Command: "stats" - View your practice statistics
- [x] Command: "update" - Update words or add sentences
- [x] Command: "clear" - Clear your wordlist
- [x] Styling: Modern terminal app with Rich
- [x] CLI standards: All commands support --help

## Usage

```bash
# Add words to your wordlist
spellwell add apple --sentence "I eat an apple every day."

# Add multiple words
spellwell add

# Practice your spelling
spellwell practice

# See your wordlist
spellwell list

# View your statistics
spellwell stats

# Update an existing word with a sentence
spellwell update apple --sentence "An apple a day keeps the doctor away."

# Get help
spellwell --help
```

## Tools used

- Poetry for dependency and package management
- Click for CLI
- Rich for styling
- Pytest for testing
