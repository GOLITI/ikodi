import React, { useState } from "react";
import Icon from "./Icon";

// Exemple de données pour la section "Mots de base"
const basicWordsLessons = [
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
  },
  {
    mot: "A ni sogoma",
    traduction: "Bonjour (le matin)",
    options: [
      "Bonjour (le matin)",
      "Bonne soirée",
      "Merci"
    ],
    bonneReponseIndex: 0
  }
];

import LessonVocalScreen from "./LessonVocalScreen";

export default function BasicWordsLessonFlow({ navigate, onBack }) {
  const [currentLesson, setCurrentLesson] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [coeurs, setCoeurs] = useState(4);

  const handleSelectOption = idx => setSelectedOption(idx);
  const handleContinuer = () => {
    if (currentLesson < basicWordsLessons.length - 1) {
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
      mot={basicWordsLessons[currentLesson].mot}
      traduction={basicWordsLessons[currentLesson].traduction}
      options={basicWordsLessons[currentLesson].options}
      bonneReponseIndex={basicWordsLessons[currentLesson].bonneReponseIndex}
      selectedOptionIndex={selectedOption}
      onSelectOption={handleSelectOption}
      onContinuer={handleContinuer}
      onFermer={handleFermer}
      coeurs={coeurs}
      progression={((currentLesson + 1) / basicWordsLessons.length) * 100}
      onAudio={() => {}}
    />
  );
}
