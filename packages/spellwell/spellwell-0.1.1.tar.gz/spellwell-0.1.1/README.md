# SpellWell

`SpellWell` is a CLI application which allows you to practice spelling using your own wordlist directly in your terminal.

To combat the problem of forgetting how to spell words because of autocomplete features in text editors, the `spellwell` CLI allows you to add words to your own wordlist and practice spelling them by having them blanked out in example sentences.

`SpellWell` comes with the non-feature of being completely free of AI usage and it's ran locally on your own machine. It's free and open source (MIT license).

It's therefore important that you add the correct spelled words to your wordlist.

## Quick Start

```bash
# Install
pipx install spellwell

# Add a tricky word
spellwell add accommodate --sentence "I can accommodate up to five people."

# Add more words interactively
spellwell add

# Practice your spelling
spellwell practice

# View your progress
spellwell stats
```

## Installation

### Recommended: Install with pipx (isolated environment)

```bash
# Install pipx if you don't have it already
python -m pip install --user pipx
python -m pipx ensurepath

# Install SpellWell
pipx install spellwell
```

Alternatively, install directly with pip:

```bash
pip install spellwell
```

After installation, you can use the `spellwell` command directly from your terminal.

## Features

- [x] Add words to your own wordlist with optional example sentences
- [x] Practice spelling in two different modes
- [x] Track your progress with detailed statistics
- [x] Modern, colorful terminal interface

## Commands

- **add**: Add words to your wordlist with optional example sentences
- **list**: Show all words from your wordlist
- **practice**: Practice spelling words in different modes
  - *sentence mode*: Shows example sentence with word blanked out
  - *blurred mode*: Shows the word with some letters hidden
- **stats**: View detailed statistics from your practice sessions
- **update**: Update a word or its example sentence
- **clear**: Remove specific words or clear entire wordlist
- **bulk_update**: Add example sentences to multiple existing words at once

## Usage

```bash
# Add words to your wordlist
spellwell add apple --sentence "I eat an apple every day."

# Add multiple words interactively
spellwell add

# Practice your spelling (default: 10 random words)
spellwell practice

# Practice with specific settings
spellwell practice --count 5 --mode blurred

# See your wordlist
spellwell list

# View your statistics
spellwell stats

# Update an existing word with a sentence
# The word `Apple` will be hidden when practicing
spellwell update apple --sentence "An apple a day keeps the doctor away."

# Add sentences to multiple words
spellwell bulk_update

# Remove a specific word
spellwell clear --word apple

# Clear your entire wordlist
spellwell clear --all

# Get help on any command
spellwell --help
spellwell practice --help
```

## Tools used

- Poetry for dependency and package management
- Click for CLI interface
- Rich for terminal styling
- Pytest for testing
