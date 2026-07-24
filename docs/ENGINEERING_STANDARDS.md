# POLYMATHICA Engineering Standards

## Core Principles

```
✓ NO PLACEHOLDERS
✓ NO MOCKUPS  
✓ NO FAKE TELEMETRY
✓ NO CLAIMING COMPLETE WITHOUT WORKING OUTPUT
```

These aren't suggestions. They are non-negotiable requirements for every component, every function, every PR.

## Code Quality Standards

### 1. No Incomplete Code
- Every function must be fully implemented
- Every class must have working methods
- Every module must be testable
- Placeholder implementations (stubs that print "TODO") are rejected

### 2. No Mock Data in Production
- All data must come from actual computation or real external sources
- Mock data is acceptable only in test files (`test_*.py`)
- Production code never hard-codes fake results
- Telemetry must reflect actual system behavior

### 3. Working Output Requirement
- Before marking a feature complete, it must produce measurable output
- Output must match specification
- Output must be reproducible
- Output must be validated against known-good references

### 4. Documentation Requirements
- Every public function: docstring with args, returns, raises
- Every module: module-level docstring explaining purpose
- Every class: class-level docstring with responsibilities
- Complex algorithms: inline comments explaining approach

## Workflow Standards

### Laboratory Workflow Pipeline

All experimental workflows must support this complete pipeline:

```
1. CREATE      → Define experiment parameters and configuration
2. CONFIGURE   → Set up environment and initial conditions
3. MESH        → Discretize domain or prepare data structures
4. VALIDATE    → Check configuration against governance rules
5. RUN         → Execute simulation or experiment
6. MONITOR     → Track progress and performance metrics
7. VISUALISE   → Render results in real-time
8. RECORD      → Save evidence and telemetry
9. REPLAY      → Reconstruct simulation from recorded data
10. REPORT     → Generate analysis and summaries
11. DISCUSS    → Interpret results with Olana
12. ARCHIVE    → Store in research archive
13. PUBLISH    → Generate publication-ready outputs
```

Any workflow missing steps is incomplete.

## Validation Standards

### Scientific Validation
- All numerical results must have error bounds
- All simulations must include convergence analysis
- All evidence must be traceable to computation
- All claims must be testable and reproducible

### Code Validation
- Unit tests required for all core functions
- Integration tests required for all workflows
- Performance tests required for GPU code
- Regression tests required for changes

### Evidence Validation
- All output must match expected ranges
- All output must pass statistical tests
- All output must be compared against reference solutions
- All output must be archived with metadata

## Governance Rules

### Rule 1: No Parameters Without Bounds
- Every parameter must have min/max values
- Every parameter must have a default value
- Every parameter must have documentation
- Parameter validation must occur at entry points

### Rule 2: No Computation Without Monitoring
- Every expensive operation must report progress
- Every operation must track resource usage
- Every operation must log key events
- Every operation must provide timing information

### Rule 3: No Results Without Validation
- Every result must be checked for sanity
- Every result must be compared against expected ranges
- Every result must include uncertainty estimates
- Every result must be archived with full metadata

### Rule 4: No Assumptions Without Documentation
- Assumptions must be explicitly stated
- Assumptions must be validated in code
- Assumptions must be tested in unit tests
- Assumptions must be explained in comments

## Testing Standards

### Unit Tests
- Minimum 80% code coverage
- All public APIs must be tested
- All error cases must be tested
- All edge cases must be tested

### Integration Tests
- Complete workflows must run end-to-end
- Data must flow correctly through pipeline
- All components must integrate properly
- Performance must meet requirements

### Validation Tests
- Results must match reference solutions
- Results must pass statistical tests
- Results must have error bounds
- Results must be reproducible

## Performance Standards

### GPU Utilization
- GPU code must achieve >80% utilization
- Memory transfers must be optimized
- Kernel launches must be minimal
- Profiling data must be available

### Execution Time
- Simulations should complete in reasonable time
- Interactive operations should respond in <1s
- Batch operations should complete in <1hr
- Long-running jobs must report progress

### Memory Usage
- Memory leaks are not acceptable
- Memory usage must scale with problem size
- Out-of-core computation supported where needed
- Memory profiling must be available

## Documentation Standards

### Code Documentation
```python
def solve_pde(equation: PDEDefinition, 
              domain: Domain, 
              boundary_conditions: Dict[str, Condition],
              solver_params: SolverParameters) -> Solution:
    """Solve a partial differential equation using finite difference method.
    
    This function discretizes the domain, applies boundary conditions,
    and solves the resulting system using the specified solver.
    
    Args:
        equation: PDE definition with coefficients and terms
        domain: Computational domain specification
        boundary_conditions: Boundary condition specifications by name
        solver_params: Solver parameters (method, tolerance, max_iter)
        
    Returns:
        Solution object with field values and metadata
        
    Raises:
        ValueError: If domain or boundary conditions are invalid
        RuntimeError: If solver fails to converge
        
    Example:
        >>> domain = Domain(bounds=[0, 1], resolution=256)
        >>> bc = {'left': Dirichlet(0), 'right': Dirichlet(1)}
        >>> params = SolverParameters(method='gmres', tol=1e-6)
        >>> solution = solve_pde(pde, domain, bc, params)
    """
```

### Architecture Documentation
- System diagrams with clear responsibilities
- Data flow diagrams for key workflows
- API specifications for all interfaces
- Configuration documentation

### Example Documentation
- Runnable examples showing common use cases
- Expected input and output
- Performance characteristics
- Common pitfalls and solutions

## Code Organization

### Module Structure
```
src/component_name/
├── __init__.py              # Public API exports
├── core.py                  # Core implementation
├── interfaces.py            # Type definitions and protocols
├── errors.py                # Custom exceptions
└── utils.py                 # Helper functions
```

### Naming Conventions
- `class_name`: PascalCase
- `function_name`: snake_case
- `CONSTANT_NAME`: UPPER_SNAKE_CASE
- `_private_name`: Leading underscore
- `__magic_method__`: Double underscore for special methods

## Review Standards

### PR Requirements
- Describe what changed and why
- Explain testing approach
- Provide performance impact analysis
- Link to relevant issues and documentation

### Review Checklist
- [ ] Code follows engineering standards
- [ ] No placeholders or mock data
- [ ] Tests pass and coverage >80%
- [ ] Documentation is complete
- [ ] Performance is acceptable
- [ ] No breaking changes without migration

## Continuous Integration

### Automated Checks
- Code style (flake8, black)
- Type checking (mypy)
- Complexity analysis (pylint)
- Unit tests (pytest)
- Integration tests
- Performance regression tests

### Status Checks
All of these must pass before merging:
- ✓ Tests
- ✓ Linting
- ✓ Type checking
- ✓ Code review
- ✓ Performance validation

## Deployment Standards

### Pre-Deployment
- All tests pass
- Documentation updated
- Performance validated
- Backward compatibility verified

### Deployment
- Automated deployment pipeline
- Gradual rollout strategy
- Health checks and monitoring
- Rollback procedures ready

### Post-Deployment
- Monitor system metrics
- Verify functionality
- Check for errors
- Gather performance data
