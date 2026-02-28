import LessonVocalScreen from "./LessonVocalScreen";
import React, { useState } from "react";

// Exemple de données pour plusieurs leçons
const lessons = [
  {
    mot: "I ni cɛ",
    traduction: "Bonjour / Merci",
    options: [
      "Comment allez-vous ?",
      "Bonjour / Merci",
      "À plus tard"
    ],
    bonneReponseIndex: 1
  },
  {
    mot: "Ka kɛnɛ wa?",
    traduction: "Comment ça va ?",
    options: [
      "Comment ça va ?",
      "Merci beaucoup",
      "Bonne nuit"
    ],
    bonneReponseIndex: 0
  }
];

export default function LearningPathVocalFlow({ navigate, onBack }) {
  const [currentLesson, setCurrentLesson] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [coeurs, setCoeurs] = useState(4);

  const handleSelectOption = idx => setSelectedOption(idx);
  const handleContinuer = () => {
    if (currentLesson < lessons.length - 1) {
      setCurrentLesson(currentLesson + 1);
      setSelectedOption(null);
    } else {
      // Retour à LearningPath ou autre action
      navigate && navigate("learningPath");
    }
  };
  const handleFermer = () => onBack ? onBack() : (navigate && navigate("learningPath"));

  return (
    <LessonVocalScreen
      mot={lessons[currentLesson].mot}
      traduction={lessons[currentLesson].traduction}
      options={lessons[currentLesson].options}
      bonneReponseIndex={lessons[currentLesson].bonneReponseIndex}
      selectedOptionIndex={selectedOption}
      onSelectOption={handleSelectOption}
      onContinuer={handleContinuer}
      onFermer={handleFermer}
      coeurs={coeurs}
      progression={((currentLesson + 1) / lessons.length) * 100}
      onAudio={() => {}}
    />
  );
}
