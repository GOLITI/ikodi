"""
Script de test pour vérifier les nouveaux proverbes authentiques ivoiriens
"""
import json
from app.orchestrator import Orchestrator
from app.models import RequeteUtilisateur

def test_proverbes():
    orchestrator = Orchestrator()
    
    # Questions de test pour vérifier différents thèmes
    questions = [
        "Parle-moi de la patience",
        "Que disent les proverbes sur le travail ?",
        "Quel conseil donner à quelqu'un d'orgueilleux ?",
        "Comment gérer les conflits en famille ?",
        "Parle-moi de la sagesse des anciens",
    ]
    
    print("╭" + "─" * 78 + "╮")
    print("│" + " 🧪 TEST DES PROVERBES AUTHENTIQUES IVOIRIENS".center(78) + "│")
    print("╰" + "─" * 78 + "╯\n")
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*80}")
        print(f"Question {i}: {question}")
        print('='*80)
        
        try:
            requete = RequeteUtilisateur(question=question)
            reponse = orchestrator.repondre(requete)
            
            print(f"\n📝 Réponse:")
            print(f"{reponse.reponse}\n")
            
            print(f"📚 Sources ({reponse.nb_sources}):")
            for j, source in enumerate(reponse.sources, 1):
                print(f"\n  [{j}] {source.titre_parent}")
                print(f"      Ethnie: {source.ethnie.value} | Type: {source.type_contenu.value}")
                print(f"      Contenu: {source.contenu[:150]}...")
                if source.morale:
                    print(f"      Morale: {source.morale[:100]}...")
                print(f"      Score similarité: {source.score:.3f}")
        
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ Tests terminés")
    print("="*80)

if __name__ == "__main__":
    test_proverbes()
