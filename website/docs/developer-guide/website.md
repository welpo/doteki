---
sidebar_position: 3
---

# Website Development

This website is built using [Docusaurus 3](https://docusaurus.io/), a static website generator.

The documentation is generated from the markdown files in the `website/docs` directory and built automatically on every commit to the `main` branch.

## Running the website locally

To run the website locally, you need to have [Node.js](https://nodejs.org/) and `npm` installed on your machine.

From the root of the repository, change directory to `website` and install the dependencies:

```bash
cd website
npm install
```

Then, run the local development server:

```bash
npx docusaurus start
```

This command should automatically open a browser window with the website running locally. If it doesn't, you should be able to access it at [http://localhost:3000/](http://localhost:3000/).
