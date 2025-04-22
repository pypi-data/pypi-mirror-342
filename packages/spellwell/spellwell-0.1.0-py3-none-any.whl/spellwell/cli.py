"""CLI module for SpellWell."""
import os
import random
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box
from . import wordlist
import re

console = Console()
DEFAULT_WORDLIST_PATH = os.path.expanduser("~/.spellwell")


@click.group()
@click.version_option()
def main():
    """SpellWell: Practice spelling using your own wordlist."""
    # Ensure the wordlist file exists
    wordlist.ensure_wordlist_exists(DEFAULT_WORDLIST_PATH)


@main.command()
@click.argument("word", required=False)
@click.option("--sentence", "-s", help="Example sentence using the word.")
@click.option("--file", "-f", default=DEFAULT_WORDLIST_PATH, help="Path to the wordlist file.")
def add(word, sentence, file):
    """Add words to your wordlist with optional example sentences."""
    if word:
        wordlist.add_word(word, file, sentence)
        console.print(f"Added '[bold green]{word}[/bold green]' to your wordlist!")
        if sentence:
            console.print(f"With example: [italic]{sentence}[/italic]")
    else:
        console.print(Panel.fit("Enter words to add to your wordlist (type 'done' when finished):", 
                               box=box.ROUNDED))
        while True:
            word = Prompt.ask("Word")
            if word.lower() == "done":
                break
            
            sentence = Prompt.ask("Example sentence (optional)", default="")
            sentence = sentence if sentence.strip() else None
            
            wordlist.add_word(word, file, sentence)
            console.print(f"Added '[bold green]{word}[/bold green]' to your wordlist!")


@main.command()
@click.option("--file", "-f", default=DEFAULT_WORDLIST_PATH, help="Path to the wordlist file.")
def list(file):
    """List all words in your wordlist."""
    words_data = wordlist.get_words_with_sentences(file)
    if not words_data:
        console.print("[yellow]Your wordlist is empty. Add some words with 'spellwell add'[/yellow]")
        return

    items = []
    for word, sentence in words_data:
        if sentence:
            items.append(f"• [cyan]{word}[/cyan]\n  [dim italic]{sentence}[/dim italic]")
        else:
            items.append(f"• [cyan]{word}[/cyan]")

    console.print(Panel.fit(
        "\n".join(items),
        title="[bold]Your Words[/bold]",
        subtitle=f"Total: {len(words_data)} words",
        box=box.ROUNDED
    ))


@main.command()
@click.option("--file", "-f", default=DEFAULT_WORDLIST_PATH, help="Path to the wordlist file.")
@click.option("--count", "-c", default=10, help="Number of words to practice.")
@click.option("--mode", "-m", type=click.Choice(['sentence', 'blurred']), default='sentence',
              help="Practice mode: 'sentence' or 'blurred'")
def practice(file, count, mode):
    """Practice spelling the words in your wordlist."""
    words_data = wordlist.get_words_with_sentences(file)
    if not words_data:
        console.print("[yellow]Your wordlist is empty. Add some words with 'spellwell add'[/yellow]")
        return
    
    if count > len(words_data):
        count = len(words_data)
    
    # If using sentence mode, filter out words without sentences
    if mode == 'sentence':
        words_with_sentences = [(word, sentence) for word, sentence in words_data if sentence]
        if not words_with_sentences:
            console.print("[yellow]No words with example sentences found. Add sentences or use 'blurred' mode.[/yellow]")
            return
        practice_data = random.sample(words_with_sentences, min(count, len(words_with_sentences)))
    else:
        practice_data = random.sample(words_data, min(count, len(words_data)))
    
    correct = 0
    results = []
    
    console.print(Panel.fit(f"Let's practice your spelling using {mode} mode!", 
                           box=box.ROUNDED))
    
    for word, sentence in practice_data:
        console.print(f"\n[bold]Here's your word:[/bold]")
        
        if mode == 'sentence':
            # Replace the word with blank in the sentence
            # We need to be careful with word boundaries and case sensitivity
            blanked_sentence = sentence.replace(word, "______")
            if blanked_sentence == sentence:  # If exact match wasn't found
                # Try case-insensitive replacement (just first occurrence)
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                blanked_sentence = pattern.sub("______", sentence, 1)
            
            console.print(f"[italic]{blanked_sentence}[/italic]")
        else:
            # Original "blurred" mode
            blurred = ''.join(['_' if i % 2 == 0 else c for i, c in enumerate(word)])
            console.print(f"[dim]{blurred}[/dim]")
        
        guess = Prompt.ask("Your spelling")
        
        if guess.lower() == word.lower():
            correct += 1
            results.append((word, guess, True))
            console.print("[green]Correct![/green]")
        else:
            results.append((word, guess, False))
            console.print(f"[red]Incorrect![/red] The correct spelling is '[bold]{word}[/bold]'")
    
    # Store results
    wordlist.store_results(results, file + ".results")
    
    # Display results
    console.print(Panel.fit(
        f"You got [bold green]{correct}[/bold green] out of [bold]{len(practice_data)}[/bold] correct!",
        title="[bold]Practice Results[/bold]",
        box=box.ROUNDED
    ))


@main.command()
@click.argument("word", required=True)
@click.option("--sentence", "-s", help="Example sentence using the word.")
@click.option("--file", "-f", default=DEFAULT_WORDLIST_PATH, help="Path to the wordlist file.")
def update(word, sentence, file):
    """Update a word or its example sentence."""
    words_data = wordlist.get_words_with_sentences(file)
    
    # Check if word exists
    for existing_word, _ in words_data:
        if existing_word.lower() == word.lower():
            wordlist.remove_word(word, file)
            wordlist.add_word(word, file, sentence)
            console.print(f"Updated '[bold green]{word}[/bold green]' in your wordlist!")
            return
    
    console.print(f"[yellow]Word '{word}' not found in your wordlist.[/yellow]")


@main.command()
@click.option("--file", "-f", default=DEFAULT_WORDLIST_PATH, help="Path to the wordlist file.")
def stats(file):
    """Show statistics from your practice sessions."""
    results_file = file + ".results"
    if not os.path.exists(results_file):
        console.print("[yellow]No practice results found yet. Start practicing with 'spellwell practice'[/yellow]")
        return
    
    all_results = wordlist.get_results(results_file)
    
    total_attempts = len(all_results)
    correct_attempts = sum(1 for _, _, correct in all_results if correct)
    
    # Group by words
    word_stats = {}
    for word, _, correct in all_results:
        if word not in word_stats:
            word_stats[word] = {"attempts": 0, "correct": 0}
        word_stats[word]["attempts"] += 1
        if correct:
            word_stats[word]["correct"] += 1
    
    # Find challenging words (less than 50% correct)
    challenging_words = [
        word for word, stats in word_stats.items()
        if stats["correct"] / stats["attempts"] < 0.5 and stats["attempts"] >= 2
    ]
    
    # Calculate success rate for each word
    for word, stats in word_stats.items():
        stats["success_rate"] = stats["correct"] / stats["attempts"]
    
    # Sort words by success rate
    sorted_words = sorted(
        [(word, stats) for word, stats in word_stats.items() if stats["attempts"] >= 2],
        key=lambda x: x[1]["success_rate"], 
        reverse=True
    )
    
    console.print(Panel.fit(
        f"Total practice attempts: [bold]{total_attempts}[/bold]\n"
        f"Correct answers: [bold green]{correct_attempts}[/bold green] "
        f"({round(correct_attempts/total_attempts*100 if total_attempts else 0)}%)\n"
        f"Words practiced: [bold]{len(word_stats)}[/bold]",
        title="[bold]Practice Statistics[/bold]",
        box=box.ROUNDED
    ))
    
    # Display top 3 most correct words
    if len(sorted_words) > 0:
        top_words = sorted_words[:min(3, len(sorted_words))]
        console.print(Panel.fit(
            "\n".join([
                f"• [green]{word}[/green]: {stats['correct']}/{stats['attempts']} "
                f"({round(stats['success_rate']*100)}%)"
                for word, stats in top_words
            ]),
            title="[bold green]Three Most Correct Words[/bold green]",
            box=box.ROUNDED
        ))
    
    # Display bottom 3 most incorrect words
    if len(sorted_words) > 0:
        bottom_words = sorted_words[max(len(sorted_words)-3, 0):]
        bottom_words.reverse()  # Show worst first
        console.print(Panel.fit(
            "\n".join([
                f"• [red]{word}[/red]: {stats['correct']}/{stats['attempts']} "
                f"({round(stats['success_rate']*100)}%)"
                for word, stats in bottom_words
            ]),
            title="[bold red]Three Most Incorrect Words[/bold red]",
            box=box.ROUNDED
        ))
    
    if challenging_words:
        console.print(Panel.fit(
            "\n".join([f"• [orange3]{word}[/orange3]" for word in challenging_words]),
            title="[bold red]Words to Focus On[/bold red]",
            box=box.ROUNDED
        ))


@main.command()
@click.option("--word", "-w", help="Specific word to remove from the wordlist.")
@click.option("--all", "clear_all", is_flag=True, help="Clear the entire wordlist.")
@click.option("--file", "-f", default=DEFAULT_WORDLIST_PATH, help="Path to the wordlist file.")
def clear(word, clear_all, file):
    """Clear words from your wordlist."""
    # Check if wordlist exists and has content
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        console.print("[yellow]Your wordlist is already empty.[/yellow]")
        return
    
    # Handle clearing a specific word
    if word:
        words_data = wordlist.get_words_with_sentences(file)
        for existing_word, _ in words_data:
            if existing_word.lower() == word.lower():
                wordlist.remove_word(word, file)
                console.print(f"[green]Word '[bold]{word}[/bold]' removed from wordlist![/green]")
                return
        console.print(f"[yellow]Word '[bold]{word}[/bold]' not found in wordlist.[/yellow]")
        return
    
    # Handle clearing all words
    if clear_all:
        if Confirm.ask("Are you sure you want to clear your entire wordlist?"):
            open(file, 'w').close()
            console.print("[green]Wordlist cleared successfully![/green]")
        return
    
    # If no option was provided, show help message
    if not (word or clear_all):
        console.print("[yellow]Please specify a word with --word or use --all to clear everything.[/yellow]")
        console.print("Run 'spellwell clear --help' for more information.")


@main.command()
@click.option("--file", "-f", default=DEFAULT_WORDLIST_PATH, help="Path to the wordlist file.")
def bulk_update(file):
    """Add example sentences to existing words in your wordlist."""
    words = wordlist.get_words(file)
    if not words:
        console.print("[yellow]Your wordlist is empty. Add some words first with 'spellwell add'[/yellow]")
        return
    
    console.print(Panel.fit("Add example sentences to your existing words:", box=box.ROUNDED))
    
    for word in words:
        console.print(f"\n[bold cyan]{word}[/bold cyan]")
        sentence = Prompt.ask("Example sentence (press Enter to skip)")
        
        if sentence.strip():
            wordlist.remove_word(word, file)
            wordlist.add_word(word, file, sentence)
            console.print(f"Updated with sentence: [dim italic]{sentence}[/dim italic]")
        else:
            console.print("[dim]Skipped[/dim]")
    
    console.print("\n[green]Finished updating words![/green]")


if __name__ == "__main__":
    main()