import clsx from "clsx";
import Heading from "@theme/Heading";
import styles from "./styles.module.css";

const FeatureList = [
  {
    title: "Easy configuration",
    imageUrl: require("@site/static/img/wizard.png").default,
    description: (
      <>
        <span className={styles.text}>dōteki</span> was designed from the ground
        up to be easily configured so your GitHub profile looks awesome in no
        time.
      </>
    ),
  },
  {
    title: "Easy to automate",
    imageUrl: require("@site/static/img/automate.png").default,
    description: (
      <>
        Set up a configuration file, add some markers to you README, and let the{" "}
        <a href="https://github.com/welpo/doteki-action">
          <span className={styles.text}>dōteki</span> GitHub Action
        </a>{" "}
        do the rest.
      </>
    ),
  },
  {
    title: "Powered by plugins",
    imageUrl: require("@site/static/img/plugins.png").default,
    description: (
      <>
        <span className={styles.text}>dōteki</span> uses Python plugins to
        gather and process the data. Use the{" "}
        <a href="/docs/category/plugins">existing plugins</a> or{" "}
        <a href="/docs/developer-guide/plugin-standard">write your own</a>!
      </>
    ),
  },
];

function Feature({ imageUrl, title, description }) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        <img src={imageUrl} className={styles.featureImg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
