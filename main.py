from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.editor_camera import EditorCamera
from ursina.shaders import basic_lighting_shader
import os
import sys


app = Ursina()
player = FirstPersonController(speed = 8, model="cube", position=Vec3(27,6,20))
player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1),)
shootables_parent = FirstPersonController
ground = Entity(model= 'plane',
                texture= 'grass',
                collider= 'mesh',
                scale= (100,1, 100))


class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent,model='cube',position=Vec3(20,1,20), color=color.red, collider='box', **kwargs)
        self.health_bar = Entity(parent=self, y=2, model='cube', color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 100
        self.hp = self.max_hp


    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return
        


    


        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        if hit_info.entity == player:
            if dist > 1:
                self.position += self.forward * time.dt * 8

            else:
                Enemy.disable(self)
                test = Text(text='game over (you got caught by red cube)', position=Vec3(0,0),wordwrap=30)
                EditorCamera()
                player.disable()



    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1

    # Enemy()
enemies = [Enemy(x=x*4) for x in range(1)]




            




        

Sky()
app.run()

vdvxc