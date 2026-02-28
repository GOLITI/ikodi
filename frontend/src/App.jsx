

import { useState, useEffect } from 'react';




import SplashScreen from './SplashScreen';
import HomeScreen from './HomeScreen';
import LearningPath from './LearningPath';
import LearningPathVocalFlow from './LearningPathVocalFlow';
import BasicWordsLessonFlow from './BasicWordsLessonFlow';
import ConversationAIScreen from './ConversationAIScreen';
import InstrumentScreen from './InstrumentScreen';
import InstrumentDetail from './InstrumentDetail';

import StoryScreen from './StoryScreen';
import ProverbScreen from './ProverbScreen';
import ConteScreen from './ConteScreen';
import SuivreSilhouetteScreen from './SuivreSilhouetteScreen';
import SuiteSilhouetteScreen from './SuiteSilhouetteScreen';


import ProgressScreen from './ProgressScreen';
import ProfileScreen from './ProfileScreen';
import LessonSystem from './LessonSystem';
import ObjetMystereScreen from './ObjetMystereScreen';

function App() {
  const [showSplash, setShowSplash] = useState(true);
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedInstrument, setSelectedInstrument] = useState(null);
  const [selectedLessonId, setSelectedLessonId] = useState(null);

  useEffect(() => {
    const timer = setTimeout(() => setShowSplash(false), 2000);
    return () => clearTimeout(timer);
  }, []);

  if (showSplash) return <SplashScreen />;


  if (showSplash) return <SplashScreen />;

  if (currentPage === 'aiConversationLesson') {
    return <ConversationAIScreen onBack={() => setCurrentPage('learningPath')} navigate={setCurrentPage} />;
  }
  if (currentPage === 'basicWordsLesson') {
    return <BasicWordsLessonFlow navigate={setCurrentPage} />;
  }
  if (currentPage === 'learningPath') {
    return <LearningPath navigate={setCurrentPage} setSelectedLessonId={setSelectedLessonId} />;
  }
  if (currentPage === 'vocalLesson') {
    return <LearningPathVocalFlow navigate={setCurrentPage} />;
  }
  if (currentPage === 'lessonSystem') {
    return (
      <LessonSystem
        lessonId={selectedLessonId}
        onBack={() => setCurrentPage('learningPath')}
        navigate={setCurrentPage}
      />
    );
  }
  if (currentPage === 'instrument') {
    return (
      <InstrumentScreen
        onBack={() => setCurrentPage('home')}
        onHome={() => setCurrentPage('home')}
        onInstrumentDetail={instrument => {
          setSelectedInstrument(instrument);
          setCurrentPage('instrumentDetail');
        }}
      />
    );
  }
  if (currentPage === 'instrumentDetail') {
    return (
      <InstrumentDetail
        onBack={() => setCurrentPage('instrument')}
        instrument={selectedInstrument}
      />
    );
  }
  if (currentPage === 'story') {
    return <StoryScreen onBack={() => setCurrentPage('home')} navigate={setCurrentPage} />;
  }
  if (currentPage === 'proverbe') {
    return <ProverbScreen onBack={() => setCurrentPage('home')} navigate={setCurrentPage} />;
  }
  if (currentPage === 'conte') {
    return <ConteScreen onBack={() => setCurrentPage('home')} navigate={setCurrentPage} />;
  }
  if (currentPage === 'suivre-silhouette') {
    return <SuivreSilhouetteScreen navigate={setCurrentPage} />;
  }
  if (currentPage === 'suite-silhouette') {
    return <SuiteSilhouetteScreen navigate={setCurrentPage} />;
  }
  if (currentPage === 'objet-mystere') {
    return <ObjetMystereScreen navigate={setCurrentPage} />;
  }
  if (currentPage === 'progress') {
    return <ProgressScreen navigate={setCurrentPage} />;
  }
  if (currentPage === 'profile') {
    return <ProfileScreen navigate={setCurrentPage} />;
  }
  return <HomeScreen navigate={setCurrentPage} />;
}

export default App;
