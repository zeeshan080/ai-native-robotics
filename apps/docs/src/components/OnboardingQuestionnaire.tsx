import React, { useState } from 'react';
import { useUser, type UserPreferences } from '../context/UserContext';
import styles from './OnboardingQuestionnaire.module.css';

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
    title: 'What is your education level?',
    description: 'This helps us adjust the complexity of explanations.',
    type: 'single',
    options: [
      { value: 'high_school', label: 'High School', description: 'Currently in or completed high school' },
      { value: 'undergraduate', label: 'Undergraduate', description: 'Currently pursuing or completed bachelor\'s degree' },
      { value: 'graduate', label: 'Graduate', description: 'Master\'s or PhD level' },
      { value: 'professional', label: 'Professional', description: 'Working professional' },
    ],
  },
  {
    id: 'programming_experience',
    title: 'What is your programming experience?',
    description: 'We\'ll adjust code examples based on your level.',
    type: 'single',
    options: [
      { value: 'none', label: 'No Experience', description: 'Never programmed before' },
      { value: 'beginner', label: 'Beginner', description: 'Learning basics, simple scripts' },
      { value: 'intermediate', label: 'Intermediate', description: 'Comfortable with one or more languages' },
      { value: 'advanced', label: 'Advanced', description: 'Professional developer or extensive experience' },
    ],
  },
  {
    id: 'robotics_background',
    title: 'Do you have any robotics background?',
    description: 'This helps us know whether to include foundational concepts.',
    type: 'boolean',
    options: [
      { value: 'true', label: 'Yes', description: 'I have worked with robots or studied robotics' },
      { value: 'false', label: 'No', description: 'Robotics is new to me' },
    ],
  },
  {
    id: 'ai_ml_experience',
    title: 'What is your AI/ML experience?',
    description: 'We\'ll adjust AI-related content accordingly.',
    type: 'single',
    options: [
      { value: 'none', label: 'No Experience', description: 'New to AI/ML' },
      { value: 'basic', label: 'Basic', description: 'Familiar with concepts' },
      { value: 'intermediate', label: 'Intermediate', description: 'Have built ML models' },
      { value: 'advanced', label: 'Advanced', description: 'Professional ML/AI experience' },
    ],
  },
  {
    id: 'learning_goals',
    title: 'What are your learning goals?',
    description: 'Select all that apply. This helps us personalize your path.',
    type: 'multi',
    options: [
      { value: 'career_change', label: 'Career Change', description: 'Transitioning into robotics' },
      { value: 'research', label: 'Research', description: 'Academic or research purposes' },
      { value: 'hobby', label: 'Hobby', description: 'Personal interest and fun' },
      { value: 'teaching', label: 'Teaching', description: 'To teach others about robotics' },
      { value: 'building_projects', label: 'Building Projects', description: 'Create real robotics projects' },
    ],
  },
  {
    id: 'preferred_language',
    title: 'What is your preferred language?',
    description: 'Content can be personalized in Urdu while keeping technical terms in English.',
    type: 'single',
    options: [
      { value: 'en', label: 'English', description: 'Content in English' },
      { value: 'ur', label: 'اردو (Urdu)', description: 'Content in Urdu with English technical terms' },
    ],
  },
];

export function OnboardingQuestionnaire(): React.ReactElement {
  const { completeOnboarding, isLoading, error } = useUser();
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Partial<Record<keyof UserPreferences, string | string[] | boolean>>>({
    learning_goals: [],
  });

  const currentQuestion = questions[currentStep];
  const isLastStep = currentStep === questions.length - 1;

  const handleSingleSelect = (value: string) => {
    if (currentQuestion.type === 'boolean') {
      setAnswers(prev => ({ ...prev, [currentQuestion.id]: value === 'true' }));
    } else {
      setAnswers(prev => ({ ...prev, [currentQuestion.id]: value }));
    }
  };

  const handleMultiSelect = (value: string) => {
    const currentValues = (answers[currentQuestion.id] as string[]) || [];
    const newValues = currentValues.includes(value)
      ? currentValues.filter(v => v !== value)
      : [...currentValues, value];
    setAnswers(prev => ({ ...prev, [currentQuestion.id]: newValues }));
  };

  const canProceed = () => {
    const answer = answers[currentQuestion.id];
    if (currentQuestion.type === 'multi') {
      return Array.isArray(answer) && answer.length > 0;
    }
    return answer !== undefined && answer !== '';
  };

  const handleNext = () => {
    if (isLastStep) {
      // Submit onboarding
      const preferences: UserPreferences = {
        education_level: answers.education_level as string,
        programming_experience: answers.programming_experience as string,
        robotics_background: answers.robotics_background as boolean,
        ai_ml_experience: answers.ai_ml_experience as string,
        learning_goals: answers.learning_goals as string[],
        preferred_language: answers.preferred_language as string,
      };
      completeOnboarding(preferences);
    } else {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handleBack = () => {
    setCurrentStep(prev => prev - 1);
  };

  const selectedValue = answers[currentQuestion.id];

  return (
    <div className={styles.container}>
      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{ width: `${((currentStep + 1) / questions.length) * 100}%` }}
        />
      </div>
      <div className={styles.stepIndicator}>
        Step {currentStep + 1} of {questions.length}
      </div>

      <div className={styles.questionCard}>
        <h2 className={styles.questionTitle}>{currentQuestion.title}</h2>
        <p className={styles.questionDescription}>{currentQuestion.description}</p>

        <div className={styles.optionsGrid}>
          {currentQuestion.options.map(option => {
            const isSelected = currentQuestion.type === 'multi'
              ? (selectedValue as string[] || []).includes(option.value)
              : currentQuestion.type === 'boolean'
                ? selectedValue === (option.value === 'true')
                : selectedValue === option.value;

            return (
              <button
                key={option.value}
                className={`${styles.optionButton} ${isSelected ? styles.optionSelected : ''}`}
                onClick={() => currentQuestion.type === 'multi'
                  ? handleMultiSelect(option.value)
                  : handleSingleSelect(option.value)
                }
                type="button"
              >
                <span className={styles.optionLabel}>{option.label}</span>
                {option.description && (
                  <span className={styles.optionDescription}>{option.description}</span>
                )}
                {currentQuestion.type === 'multi' && (
                  <span className={styles.checkbox}>
                    {isSelected ? '✓' : ''}
                  </span>
                )}
              </button>
            );
          })}
        </div>

        {error && (
          <div className={styles.error}>
            Error: {error}
          </div>
        )}

        <div className={styles.navigation}>
          {currentStep > 0 && (
            <button
              className={styles.backButton}
              onClick={handleBack}
              disabled={isLoading}
              type="button"
            >
              Back
            </button>
          )}
          <button
            className={styles.nextButton}
            onClick={handleNext}
            disabled={!canProceed() || isLoading}
            type="button"
          >
            {isLoading ? 'Saving...' : isLastStep ? 'Complete' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default OnboardingQuestionnaire;
