import neat
import pygame
import numpy as np

class NEATSimulation:
    """
    NEAT-based racing simulation that evolves neural networks to control racing cars.
    All cars drive simultaneously and are always rendered.
    """
    
    def __init__(self, start, checkpoints, screen, environment_class, world_class, max_steps, config_path="config-feedforward.txt"):
        self.config_path = config_path
        self.generation = 0
        self.world = None
        
        pygame.init()
        pygame.display.set_caption("NEAT Racing")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.start = start
        self.checkpoints = checkpoints
        
        self.max_steps = max_steps
        self.environment_class = environment_class
        self.world_class = world_class

        self.screen = screen
        
    def eval_genomes(self, genomes, config):
        """
        Evaluate all genomes in the population.
        """
        self.generation += 1
        print(f"Generation {self.generation}")
        
        if self.world is None:
            screen_width = self.screen.get_width()
            screen_height = self.screen.get_height()
            self.world = self.world_class(screen_width, screen_height, self.start, self.checkpoints)
        
        cars_data = []
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            env = self.environment_class(self.world)
            env.reset()
            cars_data.append({
                'genome_id': genome_id,
                'genome': genome,
                'net': net,
                'env': env,
                'fitness': 0
            })
        
        step = 0
        running = True
        
        while running and step < self.max_steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
            
            alive_count = 0
            for car_data in cars_data:
                if car_data['env'].car.is_alive:
                    alive_count += 1
                    
                    state = car_data['env']._get_state()
                    output = car_data['net'].activate(state)
                    action = np.argmax(output)
                    
                    _, reward, done, info = car_data['env'].step(action)
                    car_data['fitness'] += reward
                    
                    car_data['genome'].fitness = car_data['fitness']

            self._render_all_cars(cars_data, step, alive_count)
            
            if alive_count == 0:
                print(f"All cars died at step {step}")
                break
                
            step += 1
            self.clock.tick(60)
        
        for car_data in cars_data:
            car_data['genome'].fitness = car_data['fitness']
            print(f"Genome {car_data['genome_id']}: Fitness = {car_data['fitness']:.2f}")
    
    def _render_all_cars(self, cars_data, step, alive_count):
        """
        Render all cars
        """
        self.screen.fill((0, 0, 0))
        self.world.draw(self.screen)
        
        for car_data in cars_data:
            car_data['env'].car.render(self.screen)
        
        gen_text = self.font.render(f"Generation: {self.generation}", True, (255, 255, 255))
        self.screen.blit(gen_text, (10, 10))
        
        alive_text = self.font.render(f"Cars Alive: {alive_count}/{len(cars_data)}", True, (255, 255, 255))
        self.screen.blit(alive_text, (10, 50))
        
        step_text = self.font.render(f"Step: {step}/{self.max_steps}", True, (255, 255, 255))
        self.screen.blit(step_text, (10, 90))
        
        if cars_data:
            best_fitness = max(car['fitness'] for car in cars_data)
            fitness_text = self.font.render(f"Best Fitness: {best_fitness:.2f}", True, (255, 255, 255))
            self.screen.blit(fitness_text, (10, 130))
        
        pygame.display.flip()
    
    def run(self):
        """
        Run the NEAT evolution.
        """
        try:
            config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                               neat.DefaultSpeciesSet, neat.DefaultStagnation,
                               self.config_path)
            
            population = neat.Population(config)
            population.add_reporter(neat.StdOutReporter(True))
            population.run(self.eval_genomes, n=50)
            
        except KeyboardInterrupt:
            print("Simulation stopped by user")
        except Exception as e:
            print(f"Error during simulation: {e}")
        finally:
            pygame.quit()

def main():
    simulation = NEATSimulation()
    simulation.run()

if __name__ == "__main__":
    main()