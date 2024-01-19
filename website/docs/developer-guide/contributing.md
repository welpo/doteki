---
sidebar_position: 1
---

# Contributing to dōteki

Thanks for contributing to [dōteki](https://github.com/welpo/doteki). Before implementing new features and changes, please [submit an issue](https://github.com/welpo/doteki/issues/new) so that we can discuss it.

We welcome contributions in many forms, including:

- Bug reports
- Bug fixes
- Plugin suggestions
- New plugins
- Improvements to the codebase
- Documentation improvements

If you're not sure how to contribute or need help with something, please don't hesitate to reach out via the [issue tracker](https://github.com/welpo/doteki/issues) or [email](mailto:osc@osc.garden?subject=[GitHub]%20dōteki).

## Coding guidelines

- Use [`black`](https://github.com/psf/black) to format your code before submitting a pull request.
- Functions should be type annotated. Use `mypy` to check for type errors.
- Keep the code clean and maintainable. Here are some guidelines:

<details>
  <summary>Click to expand guidelines</summary>

1. **Test coverage**: Ensure comprehensive code coverage and keep tests readable. 80% coverage is the minimum; 100% is nice to have.

2. **Short, focused functions**: Keep functions brief and adhere to a single responsibility. Minimise arguments and make function signatures intuitive.

3. **Descriptive naming**: Use unambiguous names to clarify function and variable purpose.

4. **Consistent level**: Maintain one level of abstraction or focus within functions.

5. **DRY**: Don't Repeat Yourself; abstract repeated code into functions.

6. **Error handling**: Use logging and provide clear, actionable error messages.

7. **Minimal comments**: Keep code self-explanatory. Explain the why, not the how.

8. **Early returns**: Avoid deep nesting.

</details>

## Further reading

- [Setting up the Development Environment](/docs/developer-guide/)
- [How to Write a Plugin](/docs/developer-guide/plugin-standard/)
- [Updating the Documentation/Website](/docs/developer-guide/website/)

## How to submit a pull request?

- Follow the [GitHub flow](https://guides.github.com/introduction/flow/).
- Follow the [Conventional Commits specification](https://www.conventionalcommits.org/).
- Use [gitmoji](https://gitmoji.dev/) — it's fun! 🫶

## Code of conduct

We expect all contributors to follow our [Code of Conduct](https://github.com/welpo/doteki/blob/main/CODE_OF_CONDUCT.md). Please be respectful and professional when interacting with other contributors.

Thank you for your contributions!
