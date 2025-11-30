import React, { useState, useEffect } from 'react';
import { useUser, type UserPreferences } from '../context/UserContext';
import styles from './PreferencesEditor.module.css';

interface QuestionOption {
  value: string;
  label: string;
  description?: string;
}

interface Question {
  id: keyof UserPreferences;
  title: string;
  description: string;
  type: 'single' | 'multi' | 'boolean';
  options: QuestionOption[];
}

const questions: Question[] = [
  {
    id: 'education_level',
    title: 'Education Level',
    description: 'This helps us adjust the complexity of explanations.',
    type: 'single',
    options: [
      { value: 'high_school', label: 'High School' },
      { value: 'undergraduate', label: 'Undergraduate' },
      { value: 'graduate', label: 'Graduate' },
      { value: 'professional', label: 'Professional' },
    ],
  },
  {
    id: 'programming_experience',
    title: 'Programming Experience',
    description: "We'll adjust code examples based on your level.",
    type: 'single',
    options: [
      { value: 'none', label: 'No Experience' },
      { value: 'beginner', label: 'Beginner' },
      { value: 'intermediate', label: 'Intermediate' },
      { value: 'advanced', label: 'Advanced' },
    ],
  },
  {
    id: 'robotics_background',
    title: 'Robotics Background',
    description: 'Do you have any robotics experience?',
    type: 'boolean',
    options: [
      { value: 'true', label: 'Yes' },
      { value: 'false', label: 'No' },
    ],
  },
  {
    id: 'ai_ml_experience',
    title: 'AI/ML Experience',
    description: "We'll adjust AI-related content accordingly.",
    type: 'single',
    options: [
      { value: 'none', label: 'No Experience' },
      { value: 'basic', label: 'Basic' },
      { value: 'intermediate', label: 'Intermediate' },
      { value: 'advanced', label: 'Advanced' },
    ],
  },
  {
    id: 'learning_goals',
    title: 'Learning Goals',
    description: 'Select all that apply.',
    type: 'multi',
    options: [
      { value: 'career_change', label: 'Career Change' },
      { value: 'research', label: 'Research' },
      { value: 'hobby', label: 'Hobby' },
      { value: 'teaching', label: 'Teaching' },
      { value: 'building_projects', label: 'Building Projects' },
    ],
  },
  {
    id: 'preferred_language',
    title: 'Preferred Language',
    description: 'Content can be personalized in Urdu.',
    type: 'single',
    options: [
      { value: 'en', label: 'English' },
      { value: 'ur', label: 'Urdu' },
    ],
  },
];

export function PreferencesEditor(): React.ReactElement {
  const { preferences, updatePreferences, isLoading, error } = useUser();
  const [localPrefs, setLocalPrefs] = useState<Partial<UserPreferences>>({});
  const [hasChanges, setHasChanges] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Initialize local state from current preferences
  useEffect(() => {
    if (preferences) {
      setLocalPrefs({
        education_level: preferences.education_level,
        programming_experience: preferences.programming_experience,
        robotics_background: preferences.robotics_background,
        ai_ml_experience: preferences.ai_ml_experience,
        learning_goals: [...preferences.learning_goals],
        preferred_language: preferences.preferred_language,
      });
    }
  }, [preferences]);

  const handleSingleSelect = (questionId: keyof UserPreferences, value: string) => {
    const question = questions.find(q => q.id === questionId);
    if (question?.type === 'boolean') {
      setLocalPrefs(prev => ({ ...prev, [questionId]: value === 'true' }));
    } else {
      setLocalPrefs(prev => ({ ...prev, [questionId]: value }));
    }
    setHasChanges(true);
    setSaveSuccess(false);
  };

  const handleMultiSelect = (questionId: keyof UserPreferences, value: string) => {
    const currentValues = (localPrefs[questionId] as string[]) || [];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];
    setLocalPrefs(prev => ({ ...prev, [questionId]: newValues }));
    setHasChanges(true);
    setSaveSuccess(false);
  };

  const handleSave = async () => {
    // Only update fields that have changed
    const updates: Partial<UserPreferences> = {};
    if (preferences) {
      for (const key of Object.keys(localPrefs) as (keyof UserPreferences)[]) {
        const localValue = localPrefs[key];
        const currentValue = preferences[key];

        if (Array.isArray(localValue) && Array.isArray(currentValue)) {
          if (JSON.stringify(localValue.sort()) !== JSON.stringify([...currentValue].sort())) {
            updates[key] = localValue as never;
          }
        } else if (localValue !== currentValue) {
          updates[key] = localValue as never;
        }
      }
    }

    if (Object.keys(updates).length > 0) {
      await updatePreferences(updates);
      setHasChanges(false);
      setSaveSuccess(true);
    }
  };

  const handleReset = () => {
    if (preferences) {
      setLocalPrefs({
        education_level: preferences.education_level,
        programming_experience: preferences.programming_experience,
        robotics_background: preferences.robotics_background,
        ai_ml_experience: preferences.ai_ml_experience,
        learning_goals: [...preferences.learning_goals],
        preferred_language: preferences.preferred_language,
      });
      setHasChanges(false);
      setSaveSuccess(false);
    }
  };

  if (!preferences) {
    return (
      <div className={styles.container}>
        <p className={styles.loading}>Loading preferences...</p>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2 className={styles.title}>Learning Preferences</h2>
        <p className={styles.subtitle}>
          Update your preferences to get personalized content that matches your learning journey.
        </p>
      </div>

      {error && (
        <div className={styles.error}>
          Error: {error}
        </div>
      )}

      {saveSuccess && (
        <div className={styles.success}>
          Preferences saved! Your personalized content will be regenerated.
        </div>
      )}

      <div className={styles.preferencesGrid}>
        {questions.map(question => {
          const currentValue = localPrefs[question.id];

          return (
            <div key={question.id} className={styles.preferenceCard}>
              <h3 className={styles.questionTitle}>{question.title}</h3>
              <p className={styles.questionDescription}>{question.description}</p>

              <div className={styles.optionsRow}>
                {question.options.map(option => {
                  let isSelected: boolean;
                  if (question.type === 'multi') {
                    isSelected = ((currentValue as string[]) || []).includes(option.value);
                  } else if (question.type === 'boolean') {
                    isSelected = currentValue === (option.value === 'true');
                  } else {
                    isSelected = currentValue === option.value;
                  }

                  return (
                    <button
                      key={option.value}
                      className={`${styles.optionChip} ${isSelected ? styles.optionSelected : ''}`}
                      onClick={() =>
                        question.type === 'multi'
                          ? handleMultiSelect(question.id, option.value)
                          : handleSingleSelect(question.id, option.value)
                      }
                      type="button"
                    >
                      {option.label}
                      {question.type === 'multi' && isSelected && (
                        <span className={styles.checkmark}>✓</span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      <div className={styles.actions}>
        <button
          className={styles.resetButton}
          onClick={handleReset}
          disabled={!hasChanges || isLoading}
          type="button"
        >
          Reset
        </button>
        <button
          className={styles.saveButton}
          onClick={handleSave}
          disabled={!hasChanges || isLoading}
          type="button"
        >
          {isLoading ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </div>
  );
}

export default PreferencesEditor;
