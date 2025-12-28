"""
Web-6 3D IDE: Comprehensive Test Suite

Tests cover:
  - 3D entity creation and spatial mapping
  - Code-to-3D conversion (folders→planets, files→continents, etc.)
  - Spatial indexing and queries
  - Gravitational physics
  - AI agent navigation
  - Entity interaction system
  - 3D scene generation
  - Code review generation
  - Change history tracking
"""

import unittest
import math
from datetime import datetime
from aiplatform.web6_3d_ide import (
    Web6IDE, CodeTo3DMapper, Vector3, Color, Entity3D, EntityType,
    VisualizationStyle, SpatialIndexing, GravitationalPhysics,
    AIAgentNavigator, InteractionSystem, GravitationalLink
)


class TestVector3(unittest.TestCase):
    """Test 3D vector operations."""

    def test_vector_addition(self):
        """Test vector addition."""
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        result = v1 + v2

        self.assertEqual(result.x, 5)
        self.assertEqual(result.y, 7)
        self.assertEqual(result.z, 9)

    def test_vector_subtraction(self):
        """Test vector subtraction."""
        v1 = Vector3(5, 5, 5)
        v2 = Vector3(1, 2, 3)
        result = v1 - v2

        self.assertEqual(result.x, 4)
        self.assertEqual(result.y, 3)
        self.assertEqual(result.z, 2)

    def test_distance_calculation(self):
        """Test distance calculation."""
        v1 = Vector3(0, 0, 0)
        v2 = Vector3(3, 4, 0)
        distance = v1.distance_to(v2)

        self.assertAlmostEqual(distance, 5.0, places=5)

    def test_vector_normalization(self):
        """Test vector normalization."""
        v = Vector3(3, 4, 0)
        normalized = v.normalize()

        length = math.sqrt(normalized.x**2 + normalized.y**2 + normalized.z**2)
        self.assertAlmostEqual(length, 1.0, places=5)

    def test_to_tuple(self):
        """Test vector to tuple conversion."""
        v = Vector3(1, 2, 3)
        t = v.to_tuple()

        self.assertEqual(t, (1, 2, 3))


class TestEntity3D(unittest.TestCase):
    """Test 3D entity creation and properties."""

    def test_entity_creation(self):
        """Test entity creation."""
        entity = Entity3D(
            id="test_1",
            name="TestEntity",
            entity_type=EntityType.NODE,
            position=Vector3(0, 0, 0),
            size=5.0,
            color=Color(255, 0, 0)
        )

        self.assertEqual(entity.id, "test_1")
        self.assertEqual(entity.name, "TestEntity")
        self.assertEqual(entity.entity_type, EntityType.NODE)

    def test_entity_bounds(self):
        """Test entity bounding box calculation."""
        entity = Entity3D(
            id="test_1",
            name="TestEntity",
            entity_type=EntityType.BUILDING,
            position=Vector3(10, 10, 10),
            size=5.0,
            color=Color(100, 100, 100)
        )

        bounds = entity.get_bounds()

        self.assertEqual(bounds['min_x'], 5.0)
        self.assertEqual(bounds['max_x'], 15.0)
        self.assertEqual(bounds['min_y'], 5.0)
        self.assertEqual(bounds['max_y'], 15.0)

    def test_entity_distance(self):
        """Test distance between entities."""
        e1 = Entity3D(
            id="e1", name="E1", entity_type=EntityType.NODE,
            position=Vector3(0, 0, 0), size=1.0, color=Color(255, 0, 0)
        )
        e2 = Entity3D(
            id="e2", name="E2", entity_type=EntityType.NODE,
            position=Vector3(3, 4, 0), size=1.0, color=Color(0, 255, 0)
        )

        distance = e1.distance_to(e2)
        self.assertAlmostEqual(distance, 5.0, places=5)


class TestSpatialIndexing(unittest.TestCase):
    """Test spatial indexing system."""

    def setUp(self):
        self.spatial_index = SpatialIndexing(
            Vector3(-100, -100, -100),
            Vector3(100, 100, 100)
        )

    def test_add_entity(self):
        """Test adding entity to spatial index."""
        entity = Entity3D(
            id="e1", name="E1", entity_type=EntityType.NODE,
            position=Vector3(0, 0, 0), size=1.0, color=Color(255, 0, 0)
        )

        self.spatial_index.add_entity(entity)
        self.assertIn("e1", self.spatial_index.entities)

    def test_query_sphere(self):
        """Test spherical query."""
        entities = [
            Entity3D(
                id=f"e{i}", name=f"E{i}", entity_type=EntityType.NODE,
                position=Vector3(i*10, 0, 0), size=1.0, color=Color(255, 0, 0)
            )
            for i in range(5)
        ]

        for entity in entities:
            self.spatial_index.add_entity(entity)

        # Query sphere around origin
        results = self.spatial_index.query_sphere(Vector3(0, 0, 0), 20)

        # Should find entities within 20 units
        self.assertGreater(len(results), 0)

    def test_query_aabb(self):
        """Test axis-aligned bounding box query."""
        entity = Entity3D(
            id="e1", name="E1", entity_type=EntityType.NODE,
            position=Vector3(50, 50, 50), size=10.0, color=Color(255, 0, 0)
        )

        self.spatial_index.add_entity(entity)

        # Query box containing entity
        results = self.spatial_index.query_aabb(
            Vector3(40, 40, 40),
            Vector3(60, 60, 60)
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].id, "e1")


class TestCodeTo3DMapper(unittest.TestCase):
    """Test code to 3D mapping."""

    def setUp(self):
        self.mapper = CodeTo3DMapper(VisualizationStyle.REALISTIC)

    def test_map_simple_project(self):
        """Test mapping simple project structure."""
        project = {
            'name': 'TestProject',
            'folders': {
                'src': {
                    'files': {
                        'main.py': {
                            'lines': 100,
                            'classes': {
                                'Main': {
                                    'lines': 50,
                                    'complexity': 0.5,
                                    'methods': {
                                        'run': {'lines': 20, 'complexity': 0.3}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        entities = self.mapper.map_project(project)

        # Should have universe, planet, continent, building, node
        self.assertGreater(len(entities), 0)
        self.assertIn('universe_0', entities)

    def test_entity_type_mapping(self):
        """Test that entities have correct types."""
        project = {
            'name': 'Project',
            'folders': {
                'src': {
                    'files': {
                        'module.py': {
                            'lines': 100,
                            'classes': {
                                'MyClass': {
                                    'lines': 50,
                                    'complexity': 0.5,
                                    'methods': {
                                        'method': {'lines': 10, 'complexity': 0.2}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        entities = self.mapper.map_project(project)

        types = [e.entity_type for e in entities.values()]
        self.assertIn(EntityType.UNIVERSE, types)
        self.assertIn(EntityType.PLANET, types)
        self.assertIn(EntityType.CONTINENT, types)
        self.assertIn(EntityType.BUILDING, types)
        self.assertIn(EntityType.NODE, types)

    def test_dependency_link_creation(self):
        """Test creating dependency links."""
        self.mapper.add_dependency_link('e1', 'e2', 'import', 0.8)

        self.assertEqual(len(self.mapper.links), 1)
        self.assertEqual(self.mapper.links[0].source_id, 'e1')
        self.assertEqual(self.mapper.links[0].target_id, 'e2')


class TestGravitationalPhysics(unittest.TestCase):
    """Test gravitational physics engine."""

    def setUp(self):
        self.entities = {
            'e1': Entity3D(
                id='e1', name='E1', entity_type=EntityType.BUILDING,
                position=Vector3(0, 0, 0), size=5.0, color=Color(255, 0, 0),
                code_lines=100, complexity=0.5
            ),
            'e2': Entity3D(
                id='e2', name='E2', entity_type=EntityType.BUILDING,
                position=Vector3(100, 0, 0), size=5.0, color=Color(0, 255, 0),
                code_lines=100, complexity=0.5
            )
        }

        self.links = [
            GravitationalLink('e1', 'e2', 0.9, 'import')
        ]

    def test_force_calculation(self):
        """Test gravitational force calculation."""
        physics = GravitationalPhysics(self.entities, self.links)
        physics.calculate_forces()

        # Force should be non-zero
        force_e1 = physics.get_force('e1')
        magnitude = math.sqrt(force_e1.x**2 + force_e1.y**2 + force_e1.z**2)

        self.assertGreater(magnitude, 0)

    def test_stronger_link_greater_force(self):
        """Test that stronger links produce greater forces."""
        physics1 = GravitationalPhysics(self.entities, [
            GravitationalLink('e1', 'e2', 0.5, 'import')
        ])
        physics1.calculate_forces()
        force1_mag = math.sqrt(sum(x**2 for x in physics1.get_force('e1').to_tuple()))

        physics2 = GravitationalPhysics(self.entities, [
            GravitationalLink('e1', 'e2', 0.9, 'import')
        ])
        physics2.calculate_forces()
        force2_mag = math.sqrt(sum(x**2 for x in physics2.get_force('e1').to_tuple()))

        self.assertGreater(force2_mag, force1_mag)


class TestAIAgentNavigator(unittest.TestCase):
    """Test AI agent navigation system."""

    def setUp(self):
        self.entities = {
            'e1': Entity3D(
                id='e1', name='E1', entity_type=EntityType.NODE,
                position=Vector3(0, 0, 0), size=1.0, color=Color(255, 0, 0)
            ),
            'e2': Entity3D(
                id='e2', name='E2', entity_type=EntityType.NODE,
                position=Vector3(50, 0, 0), size=1.0, color=Color(0, 255, 0)
            )
        }

        self.spatial_index = SpatialIndexing(
            Vector3(-100, -100, -100),
            Vector3(100, 100, 100)
        )
        for entity in self.entities.values():
            self.spatial_index.add_entity(entity)

        self.navigator = AIAgentNavigator(self.entities, self.spatial_index)

    def test_create_agent(self):
        """Test agent creation."""
        agent = self.navigator.create_agent('agent1', Vector3(0, 0, 0))

        self.assertEqual(agent.agent_id, 'agent1')
        self.assertEqual(agent.position.to_tuple(), (0, 0, 0))

    def test_navigate_to_entity(self):
        """Test pathfinding to entity."""
        agent = self.navigator.create_agent('agent1', Vector3(0, 0, 0))
        path = self.navigator.navigate_to_entity('agent1', 'e2')

        self.assertGreater(len(path), 0)
        # Path should start at agent position
        self.assertEqual(path[0].to_tuple(), (0, 0, 0))

    def test_move_agent(self):
        """Test agent movement."""
        agent = self.navigator.create_agent('agent1', Vector3(0, 0, 0))
        velocity = Vector3(10, 0, 0)

        self.navigator.move_agent('agent1', velocity, dt=1.0)

        # Position should have moved
        self.assertGreater(agent.position.x, 0)

    def test_agent_view(self):
        """Test agent view."""
        agent = self.navigator.create_agent('agent1', Vector3(25, 0, 0))
        view = self.navigator.get_agent_view('agent1')

        self.assertIn('position', view)
        self.assertIn('visible_entities', view)
        # Should see nearby entities
        self.assertGreater(len(view['visible_entities']), 0)


class TestInteractionSystem(unittest.TestCase):
    """Test entity interaction system."""

    def setUp(self):
        self.entities = {
            'e1': Entity3D(
                id='e1', name='E1', entity_type=EntityType.NODE,
                position=Vector3(0, 0, 0), size=1.0, color=Color(255, 0, 0)
            ),
            'e2': Entity3D(
                id='e2', name='E2', entity_type=EntityType.BUILDING,
                position=Vector3(50, 0, 0), size=5.0, color=Color(0, 255, 0),
                children_ids=[]
            )
        }

        self.interaction = InteractionSystem(self.entities)

    def test_select_entity(self):
        """Test entity selection."""
        entity = self.interaction.select_entity('e1')

        self.assertIsNotNone(entity)
        self.assertEqual(entity.id, 'e1')

    def test_move_entity(self):
        """Test moving entity."""
        new_pos = Vector3(10, 10, 10)
        success = self.interaction.move_entity('e1', new_pos)

        self.assertTrue(success)
        self.assertEqual(self.entities['e1'].position.to_tuple(), (10, 10, 10))

    def test_modify_properties(self):
        """Test modifying entity properties."""
        properties = {'code_lines': 200, 'complexity': 0.8}
        success = self.interaction.modify_entity_properties('e1', properties)

        self.assertTrue(success)
        self.assertEqual(self.entities['e1'].code_lines, 200)
        self.assertEqual(self.entities['e1'].complexity, 0.8)

    def test_reorganize_hierarchy(self):
        """Test reorganizing entity hierarchy."""
        self.entities['e1'].parent_id = None
        success = self.interaction.reorganize_hierarchy('e1', 'e2')

        self.assertTrue(success)
        self.assertEqual(self.entities['e1'].parent_id, 'e2')
        self.assertIn('e1', self.entities['e2'].children_ids)

    def test_modification_history(self):
        """Test modification history tracking."""
        self.interaction.move_entity('e1', Vector3(5, 5, 5))
        self.interaction.modify_entity_properties('e1', {'code_lines': 50})

        history = self.interaction.get_modification_history()

        self.assertEqual(len(history), 2)


class TestWeb6IDE(unittest.TestCase):
    """Test complete Web-6 IDE system."""

    def setUp(self):
        self.ide = Web6IDE(VisualizationStyle.REALISTIC)

    def test_initialization_from_project(self):
        """Test IDE initialization from project."""
        project = {
            'name': 'TestProject',
            'folders': {
                'src': {
                    'files': {
                        'main.py': {
                            'lines': 100,
                            'classes': {
                                'Main': {
                                    'lines': 50,
                                    'complexity': 0.5,
                                    'methods': {
                                        'run': {'lines': 20, 'complexity': 0.3}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        self.ide.initialize_from_project(project)

        self.assertGreater(len(self.ide.entities), 0)
        self.assertIsNotNone(self.ide.viewport)

    def test_scene_generation(self):
        """Test 3D scene JSON generation."""
        project = {
            'name': 'Project',
            'folders': {
                'src': {'files': {'main.py': {
                    'lines': 100,
                    'classes': {
                        'Main': {
                            'lines': 50, 'complexity': 0.5,
                            'methods': {'run': {'lines': 10, 'complexity': 0.2}}
                        }
                    }
                }}}
            }
        }

        self.ide.initialize_from_project(project)
        scene = self.ide.get_3d_scene_json()

        self.assertIn('metadata', scene)
        self.assertIn('objects', scene)
        self.assertIn('links', scene)
        self.assertGreater(len(scene['objects']), 0)

    def test_code_review_generation(self):
        """Test 3D code review generation."""
        project = {
            'name': 'Project',
            'folders': {
                'src': {'files': {'main.py': {
                    'lines': 100,
                    'classes': {
                        'Main': {
                            'lines': 50, 'complexity': 0.8,
                            'methods': {'run': {'lines': 150, 'complexity': 0.9}}
                        }
                    }
                }}}
            }
        }

        self.ide.initialize_from_project(project)
        review = self.ide.generate_3d_code_review('reviewer1')

        self.assertIn('reviewer_id', review)
        self.assertIn('observations', review)
        # Should find high complexity issues
        self.assertGreater(len(review['observations']), 0)

    def test_ai_agent_creation(self):
        """Test AI agent creation."""
        project = {
            'name': 'Project',
            'folders': {'src': {'files': {'main.py': {
                'lines': 100,
                'classes': {'Main': {
                    'lines': 50, 'complexity': 0.5,
                    'methods': {'run': {'lines': 10, 'complexity': 0.2}}
                }}
            }}}}
        }

        self.ide.initialize_from_project(project)
        agent = self.ide.create_ai_agent('agent1')

        self.assertIsNotNone(agent)
        self.assertEqual(agent.agent_id, 'agent1')

    def test_physics_simulation(self):
        """Test physics simulation."""
        project = {
            'name': 'Project',
            'folders': {'src': {'files': {'main.py': {
                'lines': 100,
                'classes': {'Main': {
                    'lines': 50, 'complexity': 0.5,
                    'methods': {'run': {'lines': 10, 'complexity': 0.2}}
                }}
            }}}}
        }

        self.ide.initialize_from_project(project)
        initial_positions = {eid: e.position.to_tuple() for eid, e in self.ide.entities.items()}

        self.ide.simulate_physics(iterations=5)

        # Some entities should have moved (if there are dependencies)
        # At least check that simulation runs without error
        self.assertIsNotNone(self.ide.entities)


class TestEnd2EndWorkflow(unittest.TestCase):
    """End-to-end 3D IDE workflow tests."""

    def test_complete_project_analysis(self):
        """Test complete project analysis workflow."""
        project = {
            'name': 'WebApp',
            'folders': {
                'src': {
                    'files': {
                        'app.py': {
                            'lines': 200,
                            'classes': {
                                'Application': {
                                    'lines': 150,
                                    'complexity': 0.6,
                                    'methods': {
                                        'init': {'lines': 20, 'complexity': 0.2},
                                        'run': {'lines': 50, 'complexity': 0.7},
                                    }
                                }
                            }
                        },
                        'utils.py': {
                            'lines': 100,
                            'classes': {
                                'Helper': {
                                    'lines': 100,
                                    'complexity': 0.4,
                                    'methods': {
                                        'process': {'lines': 30, 'complexity': 0.5}
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

        # Add dependencies
        ide.add_dependency('app.py', 'utils.py', 'import')

        # Create agent
        agent = ide.create_ai_agent('code_reviewer')
        self.assertIsNotNone(agent)

        # Generate review
        review = ide.generate_3d_code_review('agent')
        self.assertGreater(len(review['observations']), 0)

        # Get scene
        scene = ide.get_3d_scene_json()
        self.assertGreater(len(scene['objects']), 0)


if __name__ == '__main__':
    unittest.main()
