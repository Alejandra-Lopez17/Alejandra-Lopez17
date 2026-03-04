from textwrap import dedent
from lib.console_manager import console_manager

hello_world = dedent(
    """
    # Machine Learning Vault
    
    Welcome to your **machine learning** vault! This is a simple example to implement the
    **entry point** for what will be the final implementation of your **Capstone Project**.

    Please, consider the following instructions before making any changes:

    - All files should be in compliance with **black** and **mypy**.
    - There are **CI/CD** jobs already configured and passing. **Keep them green until the end**.
    - The Jupyter Notebooks in the **notebooks** folder should be versioned **without output cells**.

    ## How to use black and mypy

    ```bash

    $ black .
    All done! ✨ 🍰 ✨
    N files left unchanged.

    $ mypy .
    Success: no issues found in N source files

    ```

    ## How to verify if my plain files are in compliance

    ```bash

    $ ./ci/scripts/check-ipynb-compliance.sh
    ...
    All notebooks are compliant (no outputs found)!

    $ ./ci/scripts/check-plain-compliance.sh
    ...
    All .typ, .txt, and .sh files are compliant!

    ```
    """
)


def main() -> None:
    console_manager.print_markdown(hello_world)


if __name__ == "__main__":
    main()
