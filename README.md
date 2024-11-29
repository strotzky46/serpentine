> [!NOTE]
> Initial population in progress

# serpentine
![image](https://github.com/user-attachments/assets/5f5255f8-8781-4b1c-82b8-9d6f68aad2ce)

A python package for array- and towline-shape estimation based on physical models derived from Païdoussis equation and equivalent formulations
and measurement input.

The core contains the class `Serpent()` representing a segmentation of a flexible cylinder (aka cable, hose, array, towline, ...). 
Various solvers are implemented to solve specific cases and return `Serpent`s for visualization and/or further processing. A `Serpent`
may also solve as a physical definition of the towline/array that is passed to a solver to determine its shape. In this case, the
class (to be implemented) draws from the [Array-Definition](https://github.com/sensortechcanada/Array-Definition) repo.

The scripts folder of the repo collects individual implementations and solutions using the tools of the core
package.

## Coordinates
`Serpent`s use a relative euklidian coordinate system with the x-axis pointing in the tow direction (fluid flow in -x), 
the z-direction pointing up (gravity acts in -z direction), and y completing the right-handed system (y points to port 
in the tow-vessel's context). The origin for a `Serpent` 
