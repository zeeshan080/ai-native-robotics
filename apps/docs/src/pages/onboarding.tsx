import React from 'react';
import Layout from '@theme/Layout';
import { OnboardingQuestionnaire } from '../components/OnboardingQuestionnaire';

export default function OnboardingPage(): React.ReactElement {
  return (
    <Layout
      title="Welcome - Personalize Your Learning"
      description="Complete the onboarding questionnaire to personalize your AI-Native Robotics learning experience."
    >
      <main style={{ padding: '2rem 0' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1>Welcome to AI-Native Robotics!</h1>
          <p style={{ color: 'var(--ifm-color-emphasis-600)', maxWidth: '600px', margin: '0 auto' }}>
            Help us personalize your learning experience by answering a few questions about your background and goals.
          </p>
        </div>
        <OnboardingQuestionnaire />
      </main>
    </Layout>
  );
}
