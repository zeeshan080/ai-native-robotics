import React from 'react';
import Layout from '@theme/Layout';
import { useUser } from '../context/UserContext';
import PreferencesEditor from '../components/PreferencesEditor';

function ProfileContent(): React.ReactElement {
  const { userId, onboardingCompleted, isLoading, clearUser } = useUser();

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem' }}>
        <p>Loading...</p>
      </div>
    );
  }

  if (!onboardingCompleted) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem' }}>
        <h2>Complete Onboarding First</h2>
        <p>You need to complete onboarding before you can edit your preferences.</p>
        <a href="/onboarding" style={{ color: 'var(--ifm-color-primary)' }}>
          Go to Onboarding
        </a>
      </div>
    );
  }

  return (
    <div>
      <PreferencesEditor />

      <div style={{
        maxWidth: '800px',
        margin: '2rem auto 0',
        padding: '0 2rem',
      }}>
        <div style={{
          borderTop: '1px solid var(--ifm-color-emphasis-200)',
          paddingTop: '1.5rem',
        }}>
          <h3 style={{ color: 'var(--ifm-color-emphasis-600)', fontSize: '1rem' }}>
            Account Information
          </h3>
          <p style={{
            color: 'var(--ifm-color-emphasis-500)',
            fontSize: '0.875rem',
            fontFamily: 'monospace',
          }}>
            User ID: {userId}
          </p>
          <button
            onClick={() => {
              if (confirm('This will reset your user data. Are you sure?')) {
                clearUser();
                window.location.href = '/';
              }
            }}
            style={{
              marginTop: '1rem',
              padding: '0.5rem 1rem',
              background: 'transparent',
              border: '1px solid var(--ifm-color-danger)',
              color: 'var(--ifm-color-danger)',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '0.875rem',
            }}
          >
            Reset User Data
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ProfilePage(): React.ReactElement {
  return (
    <Layout
      title="Profile"
      description="Manage your learning preferences"
    >
      <main style={{ paddingTop: '2rem', paddingBottom: '4rem' }}>
        <ProfileContent />
      </main>
    </Layout>
  );
}
