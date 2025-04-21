from mapFolding import raiseIfNoneGitHubIssueNumber3, The
from mapFolding.someAssemblyRequired import (
	ast_Identifier,
	astModuleToIngredientsFunction,
	be,
	DOT,
	extractFunctionDef,
	grab,
	ifThis,
	IngredientsFunction,
	IngredientsModule,
	LedgerOfImports,
	Make,
	NodeChanger,
	NodeTourist,
	parseLogicalPath2astModule,
	parsePathFilename2astModule,
	Then,
	str_nameDOTname,
)
from mapFolding.someAssemblyRequired.toolboxNumba import decorateCallableWithNumba, parametersNumbaLight
from mapFolding.someAssemblyRequired.transformationTools import (
	inlineFunctionDef,
	removeDataclassFromFunction,
	removeUnusedParameters,
	shatter_dataclassesDOTdataclass,
	unpackDataclassCallFunctionRepackDataclass,
	write_astModule,
	)
from pathlib import PurePath
import ast

algorithmSourceModuleHARDCODED = 'daoOfMapFolding'
sourceCallableIdentifierHARDCODED = 'count'
logicalPathInfixHARDCODED: ast_Identifier = 'syntheticModules'
theCountingIdentifierHARDCODED: ast_Identifier = 'groupsOfFolds'

def makeInitializeGroupsOfFolds():
	callableIdentifierHARDCODED = 'initializeGroupsOfFolds'
	moduleIdentifierHARDCODED: ast_Identifier = 'initializeCount'

	algorithmSourceModule = algorithmSourceModuleHARDCODED
	sourceCallableIdentifier = sourceCallableIdentifierHARDCODED
	logicalPathSourceModule = '.'.join([The.packageName, algorithmSourceModule])

	callableIdentifier = callableIdentifierHARDCODED
	logicalPathInfix = logicalPathInfixHARDCODED
	moduleIdentifier = moduleIdentifierHARDCODED

	astModule = parseLogicalPath2astModule(logicalPathSourceModule)
	countInitializeIngredients = IngredientsFunction(inlineFunctionDef(sourceCallableIdentifier, astModule)
		, LedgerOfImports(astModule))

	countInitializeIngredients.astFunctionDef.name = callableIdentifier

	dataclassInstanceIdentifier = NodeTourist(be.arg, Then.extractIt(DOT.arg)).captureLastMatch(countInitializeIngredients.astFunctionDef)
	if dataclassInstanceIdentifier is None: raise raiseIfNoneGitHubIssueNumber3
	theCountingIdentifier = theCountingIdentifierHARDCODED

	findThis = ifThis.isWhileAttributeNamespace_IdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
	doThat = grab.testAttribute(grab.andDoAllOf([
		grab.opsAttribute(Then.replaceWith([ast.Eq()])), # type: ignore
		grab.leftAttribute(grab.attrAttribute(Then.replaceWith(theCountingIdentifier))) # type: ignore
	]))
	NodeChanger(findThis, doThat).visit(countInitializeIngredients.astFunctionDef.body[0])

	initializationModule = IngredientsModule(countInitializeIngredients)

	pathFilename = PurePath(The.pathPackage, logicalPathInfix, moduleIdentifier + The.fileExtension)

	write_astModule(initializationModule, pathFilename, The.packageName)

def makeTheorem2():
	moduleIdentifierHARDCODED: ast_Identifier = 'theorem2'

	algorithmSourceModule = algorithmSourceModuleHARDCODED
	sourceCallableIdentifier = sourceCallableIdentifierHARDCODED
	logicalPathSourceModule = '.'.join([The.packageName, algorithmSourceModule])

	logicalPathInfix = logicalPathInfixHARDCODED
	moduleIdentifier = moduleIdentifierHARDCODED

	astModule = parseLogicalPath2astModule(logicalPathSourceModule)
	countTheorem2 = IngredientsFunction(inlineFunctionDef(sourceCallableIdentifier, astModule)
		, LedgerOfImports(astModule))

	dataclassInstanceIdentifier = NodeTourist(be.arg, Then.extractIt(DOT.arg)).captureLastMatch(countTheorem2.astFunctionDef)
	if dataclassInstanceIdentifier is None: raise raiseIfNoneGitHubIssueNumber3

	findThis = ifThis.isWhileAttributeNamespace_IdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
	doThat = grab.testAttribute(grab.comparatorsAttribute(Then.replaceWith([Make.Constant(4)]))) # type: ignore
	NodeChanger(findThis, doThat).visit(countTheorem2.astFunctionDef)

	findThis = ifThis.isIfAttributeNamespace_IdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
	doThat = Then.extractIt(DOT.body)
	insertLeaf = NodeTourist(findThis, doThat).captureLastMatch(countTheorem2.astFunctionDef)
	findThis = ifThis.isIfAttributeNamespace_IdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
	doThat = Then.replaceWith(insertLeaf)
	NodeChanger(findThis, doThat).visit(countTheorem2.astFunctionDef)

	findThis = ifThis.isAttributeNamespace_IdentifierGreaterThan0(dataclassInstanceIdentifier, 'leaf1ndex')
	doThat = Then.removeIt
	NodeChanger(findThis, doThat).visit(countTheorem2.astFunctionDef)

	findThis = ifThis.isAttributeNamespace_IdentifierLessThanOrEqual(dataclassInstanceIdentifier, 'leaf1ndex')
	doThat = Then.removeIt
	NodeChanger(findThis, doThat).visit(countTheorem2.astFunctionDef)

	theCountingIdentifier = theCountingIdentifierHARDCODED
	doubleTheCount = Make.AugAssign(Make.Attribute(ast.Name(dataclassInstanceIdentifier), theCountingIdentifier), ast.Mult(), Make.Constant(2))
	findThis = be.Return
	doThat = Then.insertThisAbove([doubleTheCount])
	NodeChanger(findThis, doThat).visit(countTheorem2.astFunctionDef)

	moduleTheorem2 = IngredientsModule(countTheorem2)

	pathFilename = PurePath(The.pathPackage, logicalPathInfix, moduleIdentifier + The.fileExtension)

	write_astModule(moduleTheorem2, pathFilename, The.packageName)

	return pathFilename

def numbaOnTheorem2(pathFilenameSource: PurePath):
	logicalPathInfix = logicalPathInfixHARDCODED
	sourceCallableIdentifier = sourceCallableIdentifierHARDCODED
	countNumbaTheorem2 = astModuleToIngredientsFunction(parsePathFilename2astModule(pathFilenameSource), sourceCallableIdentifier)
	dataclassName: ast.expr | None = NodeTourist(be.arg, Then.extractIt(DOT.annotation)).captureLastMatch(countNumbaTheorem2.astFunctionDef)
	if dataclassName is None: raise raiseIfNoneGitHubIssueNumber3
	dataclass_Identifier: ast_Identifier | None = NodeTourist(be.Name, Then.extractIt(DOT.id)).captureLastMatch(dataclassName)
	if dataclass_Identifier is None: raise raiseIfNoneGitHubIssueNumber3

	dataclassLogicalPathModule = None
	for moduleWithLogicalPath, listNameTuples in countNumbaTheorem2.imports.dictionaryImportFrom.items():
		for nameTuple in listNameTuples:
			if nameTuple[0] == dataclass_Identifier:
				dataclassLogicalPathModule = moduleWithLogicalPath
				break
		if dataclassLogicalPathModule:
			break
	if dataclassLogicalPathModule is None: raise raiseIfNoneGitHubIssueNumber3
	dataclassInstanceIdentifier = NodeTourist(be.arg, Then.extractIt(DOT.arg)).captureLastMatch(countNumbaTheorem2.astFunctionDef)
	if dataclassInstanceIdentifier is None: raise raiseIfNoneGitHubIssueNumber3
	shatteredDataclass = shatter_dataclassesDOTdataclass(dataclassLogicalPathModule, dataclass_Identifier, dataclassInstanceIdentifier)

	countNumbaTheorem2.imports.update(shatteredDataclass.imports)
	countNumbaTheorem2 = removeDataclassFromFunction(countNumbaTheorem2, shatteredDataclass)

	countNumbaTheorem2 = removeUnusedParameters(countNumbaTheorem2)

	countNumbaTheorem2 = decorateCallableWithNumba(countNumbaTheorem2, parametersNumbaLight)

	moduleNumbaTheorem2 = IngredientsModule(countNumbaTheorem2)
	moduleNumbaTheorem2.removeImportFromModule('numpy')

	pathFilename = pathFilenameSource.with_stem(pathFilenameSource.stem + 'Numba')

	write_astModule(moduleNumbaTheorem2, pathFilename, The.packageName)

	logicalPath: list[str] = []
	if The.packageName:
		logicalPath.append(The.packageName)
	if logicalPathInfix:
		logicalPath.append(logicalPathInfix)
	logicalPath.append(pathFilename.stem)
	moduleWithLogicalPath: str_nameDOTname = '.'.join(logicalPath)

	astImportFrom: ast.ImportFrom = Make.ImportFrom(moduleWithLogicalPath, list_astAlias=[Make.alias(countNumbaTheorem2.astFunctionDef.name)])

	return astImportFrom

def makeUnRePackDataclass(astImportFrom: ast.ImportFrom):
	moduleIdentifierHARDCODED: ast_Identifier = 'dataPacking'

	algorithmSourceModule = algorithmSourceModuleHARDCODED
	sourceCallableIdentifier = The.sourceCallableDispatcher
	logicalPathSourceModule = '.'.join([The.packageName, algorithmSourceModule])

	callableIdentifier = sourceCallableIdentifier
	logicalPathInfix = logicalPathInfixHARDCODED
	moduleIdentifier = moduleIdentifierHARDCODED

	doTheNeedful: IngredientsFunction = astModuleToIngredientsFunction(parseLogicalPath2astModule(logicalPathSourceModule), sourceCallableIdentifier)
	dataclassName: ast.expr | None = NodeTourist(be.arg, Then.extractIt(DOT.annotation)).captureLastMatch(doTheNeedful.astFunctionDef)
	if dataclassName is None: raise raiseIfNoneGitHubIssueNumber3
	dataclass_Identifier: ast_Identifier | None = NodeTourist(be.Name, Then.extractIt(DOT.id)).captureLastMatch(dataclassName)
	if dataclass_Identifier is None: raise raiseIfNoneGitHubIssueNumber3

	dataclassLogicalPathModule = None
	for moduleWithLogicalPath, listNameTuples in doTheNeedful.imports.dictionaryImportFrom.items():
		for nameTuple in listNameTuples:
			if nameTuple[0] == dataclass_Identifier:
				dataclassLogicalPathModule = moduleWithLogicalPath
				break
		if dataclassLogicalPathModule:
			break
	if dataclassLogicalPathModule is None: raise raiseIfNoneGitHubIssueNumber3
	dataclassInstanceIdentifier = NodeTourist(be.arg, Then.extractIt(DOT.arg)).captureLastMatch(doTheNeedful.astFunctionDef)
	if dataclassInstanceIdentifier is None: raise raiseIfNoneGitHubIssueNumber3
	shatteredDataclass = shatter_dataclassesDOTdataclass(dataclassLogicalPathModule, dataclass_Identifier, dataclassInstanceIdentifier)

	doTheNeedful.imports.update(shatteredDataclass.imports)
	doTheNeedful.imports.addAst(astImportFrom)
	targetCallableIdentifier = astImportFrom.names[0].name
	doTheNeedful = unpackDataclassCallFunctionRepackDataclass(doTheNeedful, targetCallableIdentifier, shatteredDataclass)
	targetFunctionDef = extractFunctionDef(parseLogicalPath2astModule(astImportFrom.module), targetCallableIdentifier) # type: ignore
	if targetFunctionDef is None: raise raiseIfNoneGitHubIssueNumber3
	astTuple: ast.Tuple | None = NodeTourist(be.Return, Then.extractIt(DOT.value)).captureLastMatch(targetFunctionDef)
	if astTuple is None: raise raiseIfNoneGitHubIssueNumber3
	astTuple.ctx = ast.Store()

	findThis = ifThis.isAssignAndValueIs(ifThis.isCall_Identifier(targetCallableIdentifier))
	doThat = Then.replaceWith(Make.Assign(listTargets=[astTuple], value=Make.Call(Make.Name(targetCallableIdentifier), astTuple.elts)))
	NodeChanger(findThis, doThat).visit(doTheNeedful.astFunctionDef)

	moduleDoTheNeedful = IngredientsModule(doTheNeedful)
	moduleDoTheNeedful.removeImportFromModule('numpy')

	pathFilename = PurePath(The.pathPackage, logicalPathInfix, moduleIdentifier + The.fileExtension)

	write_astModule(moduleDoTheNeedful, pathFilename, The.packageName)

if __name__ == '__main__':
	makeInitializeGroupsOfFolds()
	pathFilename = makeTheorem2()
	astImportFrom = numbaOnTheorem2(pathFilename)
	makeUnRePackDataclass(astImportFrom)
