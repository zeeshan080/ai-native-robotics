# Robotics Safety Checklist

## URDF Safety

### Joint Limits
- [ ] All revolute joints have `<limit>` element
- [ ] Lower and upper position limits are realistic
- [ ] Effort (torque) limits are specified
- [ ] Velocity limits are specified
- [ ] Limits match physical robot capabilities

### Physical Properties
- [ ] All links have `<inertial>` properties
- [ ] Mass values are realistic (not 0 or extremely large)
- [ ] Inertia tensors are positive definite
- [ ] Collision geometries are defined
- [ ] No self-collision configurations possible

### Documentation
- [ ] Safety limits are commented in URDF
- [ ] Units are documented (SI standard)
- [ ] Dangerous joints are highlighted

## ROS 2 Node Safety

### Error Handling
- [ ] All callbacks have try/except blocks
- [ ] Errors are logged appropriately
- [ ] Node gracefully handles shutdown
- [ ] Invalid messages are rejected

### Timing
- [ ] Watchdog timers for critical systems
- [ ] Timeout handling for services
- [ ] Rate limiting on publishers
- [ ] Stale data detection

### State Management
- [ ] State machine for complex operations
- [ ] Invalid state transitions prevented
- [ ] Current state is logged
- [ ] Recovery from error states

## Simulation vs Real Hardware

### Content Markers
- [ ] Simulation-only content clearly marked
- [ ] Real hardware warnings present
- [ ] Supervised operation notes included
- [ ] Hardware differences documented

### Parameter Safety
- [ ] Default parameters are safe
- [ ] Dangerous parameters require explicit override
- [ ] Parameter validation before use
- [ ] Parameter ranges documented

## Educational Content Safety

### Warnings
- [ ] "Do not run on real hardware without supervision" warning
- [ ] Hardware damage risks explained
- [ ] Personal injury risks mentioned
- [ ] Emergency procedures referenced

### Prerequisites
- [ ] Required knowledge listed
- [ ] Safety training prerequisites noted
- [ ] Equipment requirements specified
- [ ] Supervision requirements stated

## Code Review Checklist

### Before Publishing
- [ ] All safety items above checked
- [ ] Peer review completed
- [ ] Simulation testing passed
- [ ] Documentation reviewed

### Common Issues to Flag

| Issue | Risk Level | Action |
|-------|------------|--------|
| Missing joint limits | HIGH | Block until fixed |
| No error handling | MEDIUM | Require fix |
| Missing simulation warning | MEDIUM | Add warning |
| Hardcoded unsafe values | HIGH | Block until fixed |
| Missing inertial | MEDIUM | Add default |

## Emergency Stop Considerations

For any content involving motion:

- [ ] E-stop behavior documented
- [ ] Safe stop state defined
- [ ] Recovery procedure described
- [ ] Hardware E-stop referenced
