# DAG visualization for debate workflow
from workflow import create_debate_workflow


def generate_dag_mermaid():
    try:
        app = create_debate_workflow()
        
        # Get the graph and generate Mermaid
        mermaid_diagram = app.get_graph().draw_mermaid()
        
        # Save to file
        with open('debate_dag.mmd', 'w', encoding='utf-8') as f:
            f.write(mermaid_diagram)
        
        print("Mermaid diagram saved to: debate_dag.mmd")
        print("\nView online at: https://mermaid.live")
        print("\nDiagram:")
        print(mermaid_diagram)
        
        return mermaid_diagram
        
    except Exception as e:
        print(f"Error generating DAG: {str(e)}")
        return None


def generate_dag_ascii():
    pass


if __name__ == "__main__":
    print("Generating Debate System DAG...")
    print("=" * 60)
    
    # Generate ASCII version
    generate_dag_ascii()
    
    # Generate Mermaid version
    print("\\n" + "=" * 60)
    generate_dag_mermaid()
