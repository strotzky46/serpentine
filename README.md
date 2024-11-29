> [!NOTE]
> Initial population in progress

# serpentine

A python package for array- and towline-shape estimation based on physical models derived from Païdoussis equation and equivalent formulations
and measurement input.

The core contains the class `Serpent()` representing a segmentation of a flexible cylinder (aka cable, hose, array, towline, ...). 
Various solvers are implemented to solve specific cases and return `Serpent`s for visualization and/or further processing. A `Serpent`
may also solve as a physical definition of the towline/array that is passed to a solver to determine its shape. In this case, the
class (to be implemented) draws from the [Array-Definition](https://github.com/sensortechcanada/Array-Definition) repo.

The scripts folder of the repo collects individual implementations and solutions using the tools of the core
package.