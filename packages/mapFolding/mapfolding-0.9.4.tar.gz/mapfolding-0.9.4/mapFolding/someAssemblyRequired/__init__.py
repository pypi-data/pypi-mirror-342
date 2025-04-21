"""
Code Transformation Framework for Algorithm Optimization and Testing

This package implements a comprehensive framework for programmatically analyzing,
transforming, and generating optimized Python code. It serves as the algorithmic
optimization engine for the mapFolding package, enabling the conversion of readable,
functional implementations into highly-optimized variants with verified correctness.

## Core Architecture Components

1. **AST Manipulation Tools**
   - Pattern recognition with composable predicates (ifThis)
   - Node access with consistent interfaces (DOT)
   - AST traversal and transformation (NodeChanger, NodeTourist)
   - AST construction with sane defaults (Make)
   - Node transformation operations (grab, Then)

2. **Container and Organization**
   - Import tracking and management (LedgerOfImports)
   - Function packaging with dependencies (IngredientsFunction)
   - Module assembly with structured components (IngredientsModule)
   - Recipe configuration for generating optimized code (RecipeSynthesizeFlow)
   - Dataclass decomposition for compatibility (ShatteredDataclass)

3. **Optimization assembly lines**
   - General-purpose Numba acceleration (makeNumbaFlow)
   - Job-specific optimization for concrete parameters (makeJobNumba)
   - Specialized component transformation (decorateCallableWithNumba)

## Integration with Testing Framework

The transformation components are extensively tested through the package's test suite,
which provides specialized fixtures and utilities for validating both the transformation
process and the resulting optimized code:

- **syntheticDispatcherFixture**: Creates and tests a complete Numba-optimized module
  using RecipeSynthesizeFlow configuration

- **test_writeJobNumba**: Tests the job-specific optimization process with RecipeJob

These fixtures enable users to test their own custom recipes and job configurations
with minimal effort. See the documentation in tests/__init__.py for details on
extending the test suite for custom implementations.

The framework balances multiple optimization levels - from general algorithmic
improvements to parameter-specific optimizations - while maintaining the ability
to verify correctness at each transformation stage through the integrated test suite.
"""

from mapFolding.someAssemblyRequired._theTypes import (
	ast_expr_Slice as ast_expr_Slice,
	ast_Identifier as ast_Identifier,
	astClassHasDOTbody as astClassHasDOTbody,
	astClassHasDOTbody_expr as astClassHasDOTbody_expr,
	astClassHasDOTbodyList_stmt as astClassHasDOTbodyList_stmt,
	astClassHasDOTnameNotName as astClassHasDOTnameNotName,
	astClassHasDOTnameNotNameAlways as astClassHasDOTnameNotNameAlways,
	astClassHasDOTnameNotNameOptionally as astClassHasDOTnameNotNameOptionally,
	astClassHasDOTtarget as astClassHasDOTtarget,
	astClassHasDOTtarget_expr as astClassHasDOTtarget_expr,
	astClassHasDOTtargetAttributeNameSubscript as astClassHasDOTtargetAttributeNameSubscript,
	astClassHasDOTvalue as astClassHasDOTvalue,
	astClassHasDOTvalue_expr as astClassHasDOTvalue_expr,
	astClassHasDOTvalue_exprNone as astClassHasDOTvalue_exprNone,
	ImaCallToName as ImaCallToName,
	intORlist_ast_type_paramORstr_orNone as intORlist_ast_type_paramORstr_orNone,
	intORstr_orNone as intORstr_orNone,
	list_ast_type_paramORstr_orNone as list_ast_type_paramORstr_orNone,
	NodeORattribute as NodeORattribute,
	str_nameDOTname as str_nameDOTname,
	个 as 个,
	)

from mapFolding.someAssemblyRequired._toolboxPython import (
	importLogicalPath2Callable as importLogicalPath2Callable,
	importPathFilename2Callable as importPathFilename2Callable,
	NodeChanger as NodeChanger,
	NodeTourist as NodeTourist,
	parseLogicalPath2astModule as parseLogicalPath2astModule,
	parsePathFilename2astModule as parsePathFilename2astModule,
	)

from mapFolding.someAssemblyRequired._toolboxAntecedents import be as be, DOT as DOT, ifThis as ifThis
from mapFolding.someAssemblyRequired._tool_Make import Make as Make
from mapFolding.someAssemblyRequired._tool_Then import grab as grab, Then as Then

from mapFolding.someAssemblyRequired._toolboxContainers import (
	IngredientsFunction as IngredientsFunction,
	IngredientsModule as IngredientsModule,
	LedgerOfImports as LedgerOfImports,
	RecipeSynthesizeFlow as RecipeSynthesizeFlow,
	ShatteredDataclass as ShatteredDataclass,
)

from mapFolding.someAssemblyRequired._toolboxAST import (
	astModuleToIngredientsFunction as astModuleToIngredientsFunction,
	extractClassDef as extractClassDef,
	extractFunctionDef as extractFunctionDef,
	)
