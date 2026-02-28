"""
Script de test pour vérifier les nouveaux contes traditionnels
"""
from app.orchestrator import Orchestrator
from app.models import RequeteUtilisateur

def test_contes():
    orchestrator = Orchestrator()
    
    # Questions de test ciblant les contes
    questions = [
        "Raconte-moi l'histoire de l'orpheline",
        "Parle-moi de Yakouba et le lion",
        "Qu'est-ce que l'histoire de l'Enfant Terrible ?",
        "Pourquoi le serpent vit dans l'eau ?",
    ]
    
    print("╭" + "─" * 78 + "╮")
    print("│" + " 🧪 TEST DES CONTES TRADITIONNELS IVOIRIENS".center(78) + "│")
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
                print(f"      Extrait: {source.contenu[:200]}...")
                if source.morale:
                    print(f"      Morale: {source.morale[:150]}...")
                print(f"      Score: {source.score:.3f}")
        
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ Tests terminés")
    print("="*80)

if __name__ == "__main__":
    test_contes()
