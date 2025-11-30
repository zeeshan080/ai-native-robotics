import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // Main sidebar for the textbook
  mainSidebar: [
    {
      type: 'doc',
      id: 'course-overview/index',
      label: 'Course Overview',
    },
    'intro',
    // Part 1: Physical AI Foundations
    // Note: Docusaurus strips numeric prefixes from doc IDs
    {
      type: 'category',
      label: 'Part 1: Physical AI Foundations',
      link: {
        type: 'doc',
        id: 'Physical-AI-Foundations/index',
      },
      items: [
        // Chapter 1: What Is Physical AI?
        {
          type: 'category',
          label: 'Chapter 1: What Is Physical AI?',
          link: {
            type: 'doc',
            id: 'Physical-AI-Foundations/what-is-physical-ai/index',
          },
          items: [
            'Physical-AI-Foundations/what-is-physical-ai/lesson-digital-vs-physical-ai',
            'Physical-AI-Foundations/what-is-physical-ai/lesson-embodiment-hypothesis',
            'Physical-AI-Foundations/what-is-physical-ai/lesson-real-world-constraints',
            'Physical-AI-Foundations/what-is-physical-ai/lab',
          ],
        },
        // Chapter 2: Sensors, Actuators & The Humanoid Body Plan
        {
          type: 'category',
          label: 'Chapter 2: Sensors & Actuators',
          link: {
            type: 'doc',
            id: 'Physical-AI-Foundations/sensors-actuators-humanoid-body/index',
          },
          items: [
            'Physical-AI-Foundations/sensors-actuators-humanoid-body/lesson-robot-sensors',
            'Physical-AI-Foundations/sensors-actuators-humanoid-body/lesson-actuators-motors',
            'Physical-AI-Foundations/sensors-actuators-humanoid-body/lesson-humanoid-body-plan',
            'Physical-AI-Foundations/sensors-actuators-humanoid-body/lab',
          ],
        },
        // Chapter 3: The Humanoid Robotics Landscape
        {
          type: 'category',
          label: 'Chapter 3: Humanoid Landscape',
          link: {
            type: 'doc',
            id: 'Physical-AI-Foundations/humanoid-robotics-landscape/index',
          },
          items: [
            'Physical-AI-Foundations/humanoid-robotics-landscape/lesson-why-humanoid',
            'Physical-AI-Foundations/humanoid-robotics-landscape/lesson-current-platforms',
            'Physical-AI-Foundations/humanoid-robotics-landscape/lesson-challenges-future',
            'Physical-AI-Foundations/humanoid-robotics-landscape/lab',
          ],
        },
        // Part 1 Summary
        'Physical-AI-Foundations/part-summary',
      ],
    },
    // Future parts will be added here:
    // {
    //   type: 'category',
    //   label: 'Part 2: ROS 2 Fundamentals',
    //   items: [...],
    // },
  ],
};

export default sidebars;
