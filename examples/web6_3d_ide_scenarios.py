"""
Web-6 3D IDE: Complete Example Scenarios

Demonstrates all capabilities:
  1. Simple project visualization
  2. Large codebase mapping
  3. Physics simulation
  4. AI agent navigation
  5. Code review in 3D
  6. Change history
  7. Dependency analysis
  8. Interactive refactoring
"""

from aiplatform.web6_3d_ide import (
    Web6IDE, VisualizationStyle, Vector3, Color, EntityType
)
import json
from datetime import datetime


# =============================================================================
# SCENARIO 1: Simple Project Visualization
# =============================================================================

def scenario_1_simple_visualization():
    """Visualize a simple Python project in 3D."""
    print("\n" + "="*70)
    print("SCENARIO 1: Simple Project Visualization")
    print("="*70)

    # Define simple project
    simple_project = {
        'name': 'SimpleCalculator',
        'folders': {
            'src': {
                'files': {
                    'calculator.py': {
                        'lines': 150,
                        'classes': {
                            'Calculator': {
                                'lines': 150,
                                'complexity': 0.5,
                                'methods': {
                                    'add': {'lines': 10, 'complexity': 0.1},
                                    'subtract': {'lines': 10, 'complexity': 0.1},
                                    'multiply': {'lines': 15, 'complexity': 0.2},
                                    'divide': {'lines': 20, 'complexity': 0.4}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Create IDE
    ide = Web6IDE(VisualizationStyle.REALISTIC)
    ide.initialize_from_project(simple_project)

    # Display statistics
    print(f"\n📊 Project Statistics:")
    print(f"   Total Entities: {len(ide.entities)}")
    print(f"   Total Links: {len(ide.mapper.links)}")
    print(f"   Project Complexity: {sum(e.complexity for e in ide.entities.values()) / len(ide.entities):.2f}")

    # Show entity types
    entity_types = {}
    for entity in ide.entities.values():
        entity_types[entity.entity_type.name] = entity_types.get(entity.entity_type.name, 0) + 1

    print(f"\n🏗️  Entity Breakdown:")
    for etype, count in entity_types.items():
        print(f"   {etype}: {count}")

    # Export scene
    scene = ide.get_3d_scene_json()
    print(f"\n💾 Scene Export:")
    print(f"   Total objects: {len(scene['objects'])}")
    print(f"   Total links: {len(scene['links'])}")
    print(f"   Scene bounds: {scene['metadata']['bounds']}")

    return ide, scene


# =============================================================================
# SCENARIO 2: Large Codebase Mapping
# =============================================================================

def scenario_2_large_codebase():
    """Map a large, complex codebase."""
    print("\n" + "="*70)
    print("SCENARIO 2: Large Codebase Mapping")
    print("="*70)

    # Complex multi-module project
    large_project = {
        'name': 'WebApplication',
        'folders': {
            'src': {
                'files': {
                    'app.py': {
                        'lines': 300,
                        'classes': {
                            'Application': {
                                'lines': 250,
                                'complexity': 0.7,
                                'methods': {
                                    '__init__': {'lines': 30, 'complexity': 0.3},
                                    'initialize': {'lines': 60, 'complexity': 0.6},
                                    'run': {'lines': 80, 'complexity': 0.8},
                                    'shutdown': {'lines': 40, 'complexity': 0.5}
                                }
                            }
                        }
                    },
                    'routes.py': {
                        'lines': 400,
                        'classes': {
                            'Router': {
                                'lines': 350,
                                'complexity': 0.8,
                                'methods': {
                                    'register_route': {'lines': 50, 'complexity': 0.5},
                                    'handle_request': {'lines': 100, 'complexity': 0.9},
                                    'dispatch': {'lines': 80, 'complexity': 0.7}
                                }
                            },
                            'RouteHandler': {
                                'lines': 200,
                                'complexity': 0.6,
                                'methods': {
                                    'get': {'lines': 40, 'complexity': 0.4},
                                    'post': {'lines': 60, 'complexity': 0.6}
                                }
                            }
                        }
                    },
                    'database.py': {
                        'lines': 500,
                        'classes': {
                            'Database': {
                                'lines': 350,
                                'complexity': 0.7,
                                'methods': {
                                    'connect': {'lines': 30, 'complexity': 0.4},
                                    'query': {'lines': 100, 'complexity': 0.8},
                                    'execute': {'lines': 80, 'complexity': 0.7},
                                    'disconnect': {'lines': 20, 'complexity': 0.3}
                                }
                            },
                            'Connection': {
                                'lines': 150,
                                'complexity': 0.6,
                                'methods': {
                                    'open': {'lines': 30, 'complexity': 0.5},
                                    'close': {'lines': 20, 'complexity': 0.3}
                                }
                            }
                        }
                    }
                }
            },
            'utils': {
                'files': {
                    'helpers.py': {
                        'lines': 200,
                        'classes': {
                            'Validator': {
                                'lines': 150,
                                'complexity': 0.5,
                                'methods': {
                                    'validate_email': {'lines': 20, 'complexity': 0.3},
                                    'validate_password': {'lines': 30, 'complexity': 0.4}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    # Create and initialize IDE
    ide = Web6IDE(VisualizationStyle.NETWORK)
    ide.initialize_from_project(large_project)

    # Add inter-module dependencies
    ide.add_dependency('app.py', 'routes.py', 'import')
    ide.add_dependency('routes.py', 'database.py', 'import')
    ide.add_dependency('routes.py', 'helpers.py', 'import')
    ide.add_dependency('app.py', 'database.py', 'import')

    # Display analysis
    print(f"\n📊 Large Codebase Statistics:")
    print(f"   Total Entities: {len(ide.entities)}")
    print(f"   Total Dependencies: {len(ide.mapper.links)}")
    print(f"   Modules: 3 (src, src/routes, utils)")
    print(f"   Classes: 6")
    print(f"   Methods: 17")

    # Calculate metrics
    avg_complexity = sum(e.complexity for e in ide.entities.values()) / len(ide.entities)
    total_lines = sum(e.code_lines for e in ide.entities.values() if e.entity_type != EntityType.UNIVERSE)

    print(f"\n📈 Code Metrics:")
    print(f"   Average Complexity: {avg_complexity:.2f}")
    print(f"   Total Lines: {total_lines}")
    print(f"   Average Lines per Entity: {total_lines / (len(ide.entities) - 1):.0f}")

    return ide


# =============================================================================
# SCENARIO 3: Physics Simulation
# =============================================================================

def scenario_3_physics_simulation():
    """Demonstrate physics simulation with dependencies."""
    print("\n" + "="*70)
    print("SCENARIO 3: Physics Simulation with Gravitational Dependencies")
    print("="*70)

    project = {
        'name': 'PhysicsDemo',
        'folders': {
            'core': {
                'files': {
                    'engine.py': {
                        'lines': 500,
                        'classes': {
                            'Engine': {
                                'lines': 500,
                                'complexity': 0.8,
                                'methods': {
                                    'simulate': {'lines': 200, 'complexity': 0.9}
                                }
                            }
                        }
                    },
                    'physics.py': {
                        'lines': 400,
                        'classes': {
                            'Physics': {
                                'lines': 400,
                                'complexity': 0.7,
                                'methods': {
                                    'calculate_forces': {'lines': 150, 'complexity': 0.8}
                                }
                            }
                        }
                    },
                    'utils.py': {
                        'lines': 200,
                        'classes': {
                            'Utils': {
                                'lines': 200,
                                'complexity': 0.3,
                                'methods': {}
                            }
                        }
                    }
                }
            }
        }
    }

    ide = Web6IDE(VisualizationStyle.REALISTIC)
    ide.initialize_from_project(project)

    # Add strong dependencies
    ide.add_dependency('engine.py', 'physics.py', 'import')
    ide.add_dependency('physics.py', 'utils.py', 'import')
    ide.add_dependency('engine.py', 'utils.py', 'import')

    print(f"\n🌍 Initial State:")
    print(f"   Entities: {len(ide.entities)}")
    print(f"   Dependencies: {len(ide.mapper.links)}")

    # Show initial positions
    print(f"\n📍 Initial Positions:")
    for entity_id, entity in list(ide.entities.items())[:5]:
        print(f"   {entity.name}: ({entity.position.x:.1f}, {entity.position.y:.1f}, {entity.position.z:.1f})")

    # Simulate physics
    print(f"\n⚡ Running Physics Simulation...")
    for iteration in range(10):
        ide.simulate_physics(iterations=1)
        print(f"   Iteration {iteration + 1}/10", end='\r')

    print(f"\n📍 Final Positions (after physics):")
    for entity_id, entity in list(ide.entities.items())[:5]:
        print(f"   {entity.name}: ({entity.position.x:.1f}, {entity.position.y:.1f}, {entity.position.z:.1f})")

    # Analyze forces
    print(f"\n💪 Force Analysis:")
    physics = ide.physics
    for link in ide.mapper.links:
        source = ide.entities[link.source_id]
        target = ide.entities[link.target_id]
        force = physics.get_force(link.source_id)
        magnitude = (force.x**2 + force.y**2 + force.z**2)**0.5
        print(f"   {source.name} → {target.name}: Force = {magnitude:.2f}")

    return ide


# =============================================================================
# SCENARIO 4: AI Agent Navigation
# =============================================================================

def scenario_4_ai_agent_navigation():
    """Demonstrate AI agent navigating through codebase."""
    print("\n" + "="*70)
    print("SCENARIO 4: AI Agent Navigation")
    print("="*70)

    project = {
        'name': 'NavigationDemo',
        'folders': {
            'src': {
                'files': {
                    'main.py': {
                        'lines': 200,
                        'classes': {
                            'Main': {
                                'lines': 200,
                                'complexity': 0.6,
                                'methods': {
                                    'run': {'lines': 100, 'complexity': 0.7}
                                }
                            }
                        }
                    },
                    'handler.py': {
                        'lines': 300,
                        'classes': {
                            'Handler': {
                                'lines': 300,
                                'complexity': 0.8,
                                'methods': {
                                    'process': {'lines': 150, 'complexity': 0.8}
                                }
                            }
                        }
                    },
                    'database.py': {
                        'lines': 250,
                        'classes': {
                            'Database': {
                                'lines': 250,
                                'complexity': 0.7,
                                'methods': {
                                    'query': {'lines': 100, 'complexity': 0.7}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    ide = Web6IDE(VisualizationStyle.REALISTIC)
    ide.initialize_from_project(project)

    # Create AI agent
    print(f"\n🤖 Creating AI Agent...")
    agent = ide.create_ai_agent('explorer_1')
    print(f"   Agent created: {agent.agent_id}")
    print(f"   Starting position: ({agent.position.x:.1f}, {agent.position.y:.1f}, {agent.position.z:.1f})")

    # Get initial view
    initial_view = ide.navigator.get_agent_view(agent.agent_id)
    print(f"   Initial visible entities: {len(initial_view['visible_entities'])}")

    # Find target
    target_entity_id = None
    for entity_id, entity in ide.entities.items():
        if entity.name == 'Handler':
            target_entity_id = entity_id
            break

    if target_entity_id:
        print(f"\n🎯 Navigating to: Handler")

        # Plan path
        path = ide.navigator.navigate_to_entity(agent.agent_id, target_entity_id)
        print(f"   Path length: {len(path)} waypoints")

        # Move along path
        print(f"\n👣 Moving agent...")
        for i, waypoint in enumerate(path[::max(1, len(path)//10)]):  # Show 10 intermediate positions
            ide.navigator.move_agent(agent.agent_id, 
                                   Vector3(10, 0, 0), dt=0.016)
            view = ide.navigator.get_agent_view(agent.agent_id)
            progress = (i / max(1, len(path)//10)) * 100
            print(f"   Progress: {progress:.0f}% | Visible entities: {len(view['visible_entities'])}")

    # Final analysis
    final_view = ide.navigator.get_agent_view(agent.agent_id)
    print(f"\n📊 Final Agent State:")
    print(f"   Position: ({agent.position.x:.1f}, {agent.position.y:.1f}, {agent.position.z:.1f})")
    print(f"   Visible entities: {len(final_view['visible_entities'])}")
    print(f"   Visited locations: {len(agent.visited_entities)}")

    return ide


# =============================================================================
# SCENARIO 5: Code Review in 3D
# =============================================================================

def scenario_5_code_review():
    """Generate code review using 3D analysis."""
    print("\n" + "="*70)
    print("SCENARIO 5: Code Review in 3D")
    print("="*70)

    project = {
        'name': 'ReviewTarget',
        'folders': {
            'src': {
                'files': {
                    'complex_logic.py': {
                        'lines': 500,
                        'classes': {
                            'ComplexProcessor': {
                                'lines': 500,
                                'complexity': 0.95,  # Very high complexity
                                'methods': {
                                    'process_data': {'lines': 300, 'complexity': 0.95},
                                    'validate': {'lines': 100, 'complexity': 0.8}
                                }
                            }
                        }
                    },
                    'utils.py': {
                        'lines': 100,
                        'classes': {
                            'Utils': {
                                'lines': 100,
                                'complexity': 0.3,
                                'methods': {
                                    'helper': {'lines': 50, 'complexity': 0.2}
                                }
                            }
                        }
                    },
                    'tightly_coupled.py': {
                        'lines': 200,
                        'classes': {
                            'Coupled': {
                                'lines': 200,
                                'complexity': 0.6,
                                'methods': {}
                            }
                        }
                    }
                }
            }
        }
    }

    ide = Web6IDE(VisualizationStyle.REALISTIC)
    ide.initialize_from_project(project)

    # Add tightly coupled dependencies
    ide.add_dependency('complex_logic.py', 'utils.py', 'import')
    ide.add_dependency('complex_logic.py', 'tightly_coupled.py', 'import')
    ide.add_dependency('tightly_coupled.py', 'utils.py', 'import')

    print(f"\n👁️  Running Code Review...")

    # Generate review
    review = ide.generate_3d_code_review('ai_reviewer')

    print(f"\n📋 Review Results:")
    print(f"   Reviewer: {review['reviewer_id']}")
    print(f"   Timestamp: {review['timestamp']}")
    print(f"   Total Observations: {len(review['observations'])}")

    # High severity issues
    high_severity = [o for o in review['observations'] if o['severity'] == 'high']
    print(f"\n⚠️  HIGH SEVERITY ({len(high_severity)}):")
    for obs in high_severity[:5]:
        print(f"   • {obs['message']}")
        print(f"     → {obs['suggestion']}")

    # Medium severity issues
    med_severity = [o for o in review['observations'] if o['severity'] == 'medium']
    print(f"\n⚠️  MEDIUM SEVERITY ({len(med_severity)}):")
    for obs in med_severity[:3]:
        print(f"   • {obs['message']}")

    # Metrics
    print(f"\n📊 Metrics:")
    print(f"   Total Entities: {review['metrics']['total_entities']}")
    print(f"   High Complexity: {review['metrics']['high_complexity_count']}")
    print(f"   High Coupling: {review['metrics']['high_coupling_count']}")
    print(f"   Avg Coupling: {review['metrics']['average_coupling']:.2f}")

    return ide, review


# =============================================================================
# SCENARIO 6: Change History
# =============================================================================

def scenario_6_change_history():
    """Demonstrate change history tracking."""
    print("\n" + "="*70)
    print("SCENARIO 6: Change History & Timeline")
    print("="*70)

    project = {
        'name': 'Evolving',
        'folders': {
            'src': {
                'files': {
                    'module.py': {
                        'lines': 150,
                        'classes': {
                            'Module': {
                                'lines': 150,
                                'complexity': 0.5,
                                'methods': {
                                    'method1': {'lines': 50, 'complexity': 0.4}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    ide = Web6IDE(VisualizationStyle.REALISTIC)
    ide.initialize_from_project(project)

    print(f"\n✏️  Making Changes...")

    # Find module entity
    module_entity = None
    for entity_id, entity in ide.entities.items():
        if entity.name == 'Module':
            module_entity = entity_id
            break

    if module_entity:
        # Change 1: Move entity
        print(f"   1. Moving module...")
        ide.interaction.move_entity(module_entity, Vector3(100, 100, 100))

        # Change 2: Modify properties
        print(f"   2. Refactoring module...")
        ide.interaction.modify_entity_properties(
            module_entity,
            {'complexity': 0.3, 'code_lines': 100}
        )

        # Get history
        history = ide.interaction.get_modification_history()

        print(f"\n📜 Change History ({len(history)} changes):")
        for i, change in enumerate(history, 1):
            print(f"\n   Change {i}:")
            print(f"   • Timestamp: {change['timestamp'].strftime('%H:%M:%S')}")
            print(f"   • Entity: {change['entity_id']}")
            print(f"   • Type: {change['change_type']}")
            print(f"   • Description: {change['description']}")

    # Export timeline
    timeline = ide.get_3d_change_history()
    print(f"\n📊 Timeline Export:")
    print(f"   Project: {timeline['project_id']}")
    print(f"   Timeline events: {len(timeline['timeline'])}")

    return ide


# =============================================================================
# SCENARIO 7: Dependency Analysis
# =============================================================================

def scenario_7_dependency_analysis():
    """Analyze code dependencies in 3D space."""
    print("\n" + "="*70)
    print("SCENARIO 7: Dependency Analysis")
    print("="*70)

    project = {
        'name': 'DependencyAnalysis',
        'folders': {
            'services': {
                'files': {
                    'auth.py': {
                        'lines': 300,
                        'classes': {
                            'AuthService': {
                                'lines': 300,
                                'complexity': 0.7,
                                'methods': {}
                            }
                        }
                    },
                    'payment.py': {
                        'lines': 400,
                        'classes': {
                            'PaymentService': {
                                'lines': 400,
                                'complexity': 0.8,
                                'methods': {}
                            }
                        }
                    },
                    'notification.py': {
                        'lines': 250,
                        'classes': {
                            'NotificationService': {
                                'lines': 250,
                                'complexity': 0.6,
                                'methods': {}
                            }
                        }
                    }
                }
            },
            'utils': {
                'files': {
                    'logger.py': {
                        'lines': 100,
                        'classes': {
                            'Logger': {
                                'lines': 100,
                                'complexity': 0.3,
                                'methods': {}
                            }
                        }
                    }
                }
            }
        }
    }

    ide = Web6IDE(VisualizationStyle.NETWORK)
    ide.initialize_from_project(project)

    # Build dependency graph
    dependencies = [
        ('auth.py', 'logger.py', 'import', 0.7),
        ('payment.py', 'auth.py', 'call', 0.9),
        ('payment.py', 'logger.py', 'import', 0.6),
        ('notification.py', 'logger.py', 'import', 0.5),
        ('payment.py', 'notification.py', 'call', 0.8),
    ]

    for source, target, dtype, strength in dependencies:
        ide.add_dependency(source, target, dtype)

    print(f"\n🔗 Dependency Analysis:")
    print(f"   Total Dependencies: {len(ide.mapper.links)}")
    print(f"   Dependency Types:")

    type_counts = {}
    type_strengths = {}
    for link in ide.mapper.links:
        type_counts[link.type] = type_counts.get(link.type, 0) + 1
        if link.type not in type_strengths:
            type_strengths[link.type] = []
        type_strengths[link.type].append(link.strength)

    for dtype in type_counts:
        avg_strength = sum(type_strengths[dtype]) / len(type_strengths[dtype])
        print(f"      {dtype}: {type_counts[dtype]} (avg strength: {avg_strength:.2f})")

    # Find hub entities (high degree)
    print(f"\n⭐ Hub Entities (High Connectivity):")
    entity_connections = {}
    for link in ide.mapper.links:
        entity_connections[link.source_id] = entity_connections.get(link.source_id, 0) + 1
        entity_connections[link.target_id] = entity_connections.get(link.target_id, 0) + 1

    sorted_hubs = sorted(entity_connections.items(), key=lambda x: x[1], reverse=True)
    for entity_id, count in sorted_hubs[:3]:
        if entity_id in ide.entities:
            print(f"   • {ide.entities[entity_id].name}: {count} connections")

    return ide


# =============================================================================
# SCENARIO 8: Interactive Refactoring
# =============================================================================

def scenario_8_interactive_refactoring():
    """Interactive refactoring using 3D IDE."""
    print("\n" + "="*70)
    print("SCENARIO 8: Interactive Refactoring")
    print("="*70)

    project = {
        'name': 'MonolithicApp',
        'folders': {
            'src': {
                'files': {
                    'monolith.py': {
                        'lines': 1000,
                        'classes': {
                            'GodClass': {
                                'lines': 1000,
                                'complexity': 0.95,
                                'methods': {
                                    'do_everything': {'lines': 500, 'complexity': 0.95},
                                    'handle_users': {'lines': 200, 'complexity': 0.8},
                                    'handle_payments': {'lines': 200, 'complexity': 0.85},
                                    'handle_notifications': {'lines': 100, 'complexity': 0.7}
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    ide = Web6IDE(VisualizationStyle.REALISTIC)
    ide.initialize_from_project(project)

    print(f"\n🏛️  Before Refactoring:")
    god_class = None
    for entity_id, entity in ide.entities.items():
        if entity.name == 'GodClass':
            god_class = entity_id
            print(f"   • {entity.name}: {entity.code_lines} lines, complexity {entity.complexity:.2f}")

    # Refactoring: Extract services
    print(f"\n🔨 Refactoring Actions:")

    if god_class:
        # Split responsibilities
        actions = [
            {
                'action': 'Extract UserService',
                'method': 'handle_users',
                'new_complexity': 0.6,
                'new_lines': 200
            },
            {
                'action': 'Extract PaymentService',
                'method': 'handle_payments',
                'new_complexity': 0.7,
                'new_lines': 200
            },
            {
                'action': 'Extract NotificationService',
                'method': 'handle_notifications',
                'new_complexity': 0.5,
                'new_lines': 100
            }
        ]

        for i, action in enumerate(actions, 1):
            print(f"\n   {i}. {action['action']}")
            print(f"      • New complexity: {action['new_complexity']:.2f}")
            print(f"      • New lines: {action['new_lines']}")

        # Apply refactoring
        print(f"\n✅ Refactoring Applied:")
        ide.interaction.modify_entity_properties(
            god_class,
            {
                'complexity': 0.5,
                'code_lines': 200
            }
        )
        print(f"   • Reduced GodClass complexity to 0.5")
        print(f"   • Reduced lines to 200")

    print(f"\n📊 After Refactoring:")
    for entity_id, entity in ide.entities.items():
        if entity.name == 'GodClass':
            print(f"   • {entity.name}: {entity.code_lines} lines, complexity {entity.complexity:.2f}")

    return ide


# =============================================================================
# Main Execution
# =============================================================================

def main():
    """Run all scenarios."""
    print("\n" + "="*70)
    print("WEB-6 3D IDE: COMPREHENSIVE EXAMPLE SCENARIOS")
    print("="*70)

    try:
        # Scenario 1
        scenario_1_simple_visualization()

        # Scenario 2
        scenario_2_large_codebase()

        # Scenario 3
        scenario_3_physics_simulation()

        # Scenario 4
        scenario_4_ai_agent_navigation()

        # Scenario 5
        ide_review, review = scenario_5_code_review()

        # Scenario 6
        scenario_6_change_history()

        # Scenario 7
        scenario_7_dependency_analysis()

        # Scenario 8
        scenario_8_interactive_refactoring()

        print("\n" + "="*70)
        print("✅ ALL SCENARIOS COMPLETED SUCCESSFULLY")
        print("="*70)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
