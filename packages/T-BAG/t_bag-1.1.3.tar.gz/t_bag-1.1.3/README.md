# T-BAG (Text-Based Adventure Game)

T-BAG is a text-based RPG game where the player navigates through different rooms, collects items, and avoids
monsters to reach the garden and win the game.

## Description

In this game, you start in a hall and must navigate through different rooms, collecting items and avoiding monsters.
Your goal is to reach the garden with the key and a potion to win the game.

## Installation

1. install the module:
    ```sh
    pip install --no-cache-dir T-BAG
    ```
2. Run the game:
    ```sh
    python -m T_BAG
    ```
3. Uninstall so you can update it:
    ```sh
    pip uninstall T_BAG
    ```

## Usage

- Use the `go` command to move to a different room. For example:
    ```sh
    go east
    ```
- Use the `get` command to pick up an item. For example:
    ```sh
    get key
    ```
- Use the `quit` command to exit the game. For example:
    ```sh
    quit 5
    ```

## Commands

- `go [direction]`: Move to a different room.
- `get [item]`: Pick up an item from the room.
- `quit [seconds]`: Quit the game after waiting for the specified number of
seconds.
- `help [number]`: Show the list of commands. If a number is provided, show
that many commands; put 0 to print all the commands.
- `drop [item]`: Drop an item into the room you are in.
- `look [anything]`: Look around the room you are currently in. You can enter
anything after the `look` command, but you must enter something, because of
how I handle commands

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes. The
rules for contributing are [here](docx/CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the LICENSE file for details.
