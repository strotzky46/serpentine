> [!NOTE]
> Initial population in progress

# serpentine
![image](https://github.com/user-attachments/assets/5f5255f8-8781-4b1c-82b8-9d6f68aad2ce)



A python package for array- and towline-shape estimation based on physical models derived from Païdoussis equation and equivalent formulations
and measurement input.

The core contains the class `Serpent()` representing a segmentation of a flexible cylinder (aka cable, hose, array, towline, ...). 
Various solvers are implemented to solve specific cases and return `Serpent`s for visualization and/or further processing. A `Serpent`
may also solve as a physical definition of the towline/array that is passed to a solver to determine its shape. In this case, the
class (to be implemented) draws from the array definition repo.

The scripts folder of the repo collects individual implementations and solutions using the tools of the core
package.
