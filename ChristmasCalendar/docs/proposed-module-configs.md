# Proposed calendar module configs

Values are proposals for SHC 1.41. Merge each YAML entry under `config-sparse.modules` in `ChristmasCalendar-Settings/config.yml` after its version is available. Add the matching dependency in `ChristmasCalendar/definition.yml` at that time. The snippets use the calendar?s `suggested-value` format.

Monsterfish values are the resolved `config-full.modules` values from the installed Reconquista test configuration, including inherited defaults. Option names and baseline values come from each installed module?s `options.yml` and shipped `config.yml` where present.

Smarter Patrols 1.0.0 is excluded because AIC Tactics supersedes it.

Map Editor Improvements is an authoring tool and falls outside the calendar gameplay and player quality-of-life scope.

## smarter-buildings 1.0.12

Dependencies are `framework ^3.0.7`, `frontend ^1.0.2`, `map-extensions ^1.0.0`.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `doors.dynamic` | `true` | `true` | Recover blocked doors |
| `doors.storage` | `true` | `true` | Recover blocked deliveries |
| `doors.unstuck` | `true` | `true` | Retry worker exits |
| `repair.fire_blocks` | `true` | `true` | Keep fire restriction |
| `firemen.spread` | `true` | `true` | Distribute firefighting |
| `firemen.tiles` | `20` | `20` | Keep module default |
| `farms.keep_cows` | `false` | `true` | Keep vanilla cow loss |
| `repair.button` | `false` | `true` | Keep original repair eligibility |
| `repair.x` | `340` | `340` | Inactive with parent off |
| `repair.y` | `466` | `466` | Inactive with parent off |
| `stables.panel` | `true` | `true` | Show stable status |
| `farms.ground_overlay` | `true` | `true` | Show farm terrain |
| `repair.gold` | `false` | `true` | Keep original repair costs |
| `blacksmith.maces` | `false` | `true` | Keep weapon production |
| `stables.breed` | `false` | `true` | Keep horse production |
| `stables.breed_seconds` | `0` | `0` | Inactive with parent off |
| `stables.slowdown` | `false` | `true` | Keep horse replenishment |
| `stables.normal_horses` | `4` | `4` | Inactive with parent off |
| `stables.slowdown_factor` | `3` | `3` | Inactive with parent off |
| `stables.slowest_seconds` | `600` | `600` | Inactive with parent off |
| `farms.dairy_scrub` | `false` | `true` | Keep dairy terrain rules |
| `hunters.tannery` | `false` | `true` | Keep leather supply |
| `hunters.chance` | `50` | `50` | Inactive with parent off |
| `hunters.carry` | `2` | `2` | Inactive with parent off |
| `hunters.stored` | `4` | `4` | Inactive with parent off |
| `repair.ai` | `false` | `true` | Keep AI repair policy |
| `repair.ai_damage` | `20` | `5` | Inactive with parent off |
| `repair.ai_interval` | `60` | `60` | Inactive with parent off |
| `repair.ai_minimum_gold` | `2000` | `2000` | Inactive with parent off |
| `ai.decorations` | `true` | `true` | Avoid stacked decorations |

```yaml
smarter-buildings:
  config:
    doors:
      dynamic:
        contents:
          suggested-value: true
      storage:
        contents:
          suggested-value: true
      unstuck:
        contents:
          suggested-value: true
    repair:
      fire_blocks:
        contents:
          suggested-value: true
      button:
        contents:
          suggested-value: false
      x:
        contents:
          suggested-value: 340
      y:
        contents:
          suggested-value: 466
      gold:
        contents:
          suggested-value: false
      ai:
        contents:
          suggested-value: false
      ai_damage:
        contents:
          suggested-value: 20
      ai_interval:
        contents:
          suggested-value: 60
      ai_minimum_gold:
        contents:
          suggested-value: 2000
    firemen:
      spread:
        contents:
          suggested-value: true
      tiles:
        contents:
          suggested-value: 20
    farms:
      keep_cows:
        contents:
          suggested-value: false
      ground_overlay:
        contents:
          suggested-value: true
      dairy_scrub:
        contents:
          suggested-value: false
    stables:
      panel:
        contents:
          suggested-value: true
      breed:
        contents:
          suggested-value: false
      breed_seconds:
        contents:
          suggested-value: 0
      slowdown:
        contents:
          suggested-value: false
      normal_horses:
        contents:
          suggested-value: 4
      slowdown_factor:
        contents:
          suggested-value: 3
      slowest_seconds:
        contents:
          suggested-value: 600
    blacksmith:
      maces:
        contents:
          suggested-value: false
    hunters:
      tannery:
        contents:
          suggested-value: false
      chance:
        contents:
          suggested-value: 50
      carry:
        contents:
          suggested-value: 2
      stored:
        contents:
          suggested-value: 4
    ai:
      decorations:
        contents:
          suggested-value: true
```

## smarter-gatehouses 1.0.8

Dependencies are `framework ^3.0.7`, `frontend ^1.0.2`, `map-extensions ^1.0.0`, `route-search ^1.0.0`.

Set ucp2-legacy.o_responsivegates.enabled to false when enabling this profile so gate detection has one owner. The retry cache applies only when the stairs rule is enabled.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `pathing.enemy_gates_closed` | `true` | `true` | Avoid blocked enemy routes |
| `pathing.remember_blocked` | `true` | `true` | Avoid repeated route searches |
| `pathing.remember_ticks` | `100` | `100` | Keep module default |
| `detection.centred` | `true` | `true` | Symmetric gate detection |
| `detection.reachable_only` | `true` | `true` | Ignore disconnected enemies |
| `walls.stairs_needed` | `false` | `false` | Keep human wall access |
| `walls.stairs_needed_ai` | `false` | `false` | Keep AI wall access |
| `walls.assassins_climb` | `true` | `true` | Preserve climbing exemption |
| `damage.large_gatehouse` | `100` | `100` | Full original ranged damage |

```yaml
smarter-gatehouses:
  config:
    pathing:
      enemy_gates_closed:
        contents:
          suggested-value: true
      remember_blocked:
        contents:
          suggested-value: true
      remember_ticks:
        contents:
          suggested-value: 100
    detection:
      centred:
        contents:
          suggested-value: true
      reachable_only:
        contents:
          suggested-value: true
    walls:
      stairs_needed:
        contents:
          suggested-value: false
      stairs_needed_ai:
        contents:
          suggested-value: false
      assassins_climb:
        contents:
          suggested-value: true
    damage:
      large_gatehouse:
        contents:
          suggested-value: 100
```

## smarter-pathing 1.0.5

Dependencies are `map-extensions ^1.0.0`, `route-search ^1.0.0`, `framework ^3.0.7`, `frontend ^1.0.2`.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `assassinsResume` | `true` | `true` | Resume interrupted routes |
| `workersUnstuck` | `true` | `true` | Recover stalled workers |
| `workersJobsUnstuck` | `true` | `true` | Recover stalled jobs |
| `rebuildLimit` | `true` | `true` | Limit repeated search rebuilds |
| `rebuildEveryTicks` | `200` | `200` | Keep module default |
| `ignoreQuarryPiles` | `false` | `true` | Keep quarry pile routing |
| `assassinsShortcut` | `false` | `true` | Keep original climb routes |
| `shortcutGroundSteps` | `30` | `30` | Inactive with parent off |
| `shortcutSavingPercent` | `25` | `25` | Inactive with parent off |

```yaml
smarter-pathing:
  config:
    assassinsResume:
      contents:
        suggested-value: true
    workersUnstuck:
      contents:
        suggested-value: true
    workersJobsUnstuck:
      contents:
        suggested-value: true
    rebuildLimit:
      contents:
        suggested-value: true
    rebuildEveryTicks:
      contents:
        suggested-value: 200
    ignoreQuarryPiles:
      contents:
        suggested-value: false
    assassinsShortcut:
      contents:
        suggested-value: false
    shortcutGroundSteps:
      contents:
        suggested-value: 30
    shortcutSavingPercent:
      contents:
        suggested-value: 25
```

## smarter-recruits 1.0.11

Dependencies are `framework >=3.0.7`, `frontend >=1.0.2`, `textResourceModifier ^0.3.0`.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `horse_archers.shoot_on_the_way` | `false` | `true` | Keep mounted firing behavior |
| `rally.keep_new_orders` | `true` | `true` | Respect manual orders |
| `rally.terrain_speed` | `true` | `true` | Respect terrain speed |
| `rally.monks_fix` | `true` | `true` | Repair monk rally behavior |
| `horse_archers.ride_on` | `false` | `true` | Keep mounted movement behavior |
| `rally.fight_on_the_way` | `false` | `true` | Keep original rally combat |
| `rally.follow_changes` | `true` | `true` | Follow updated rally point |
| `rally.run_when_aggressive` | `false` | `true` | Keep original rally speed |
| `rally.buttons` | `true` | `true` | Expose rally controls |
| `stance.button` | `true` | `true` | Expose stance controls |
| `stance.start` | `"normal"` | `"normal"` | Keep normal starting stance |
| `debug.log` | `false` | `true` | Disable diagnostic logging |

```yaml
smarter-recruits:
  config:
    horse_archers:
      shoot_on_the_way:
        contents:
          suggested-value: false
      ride_on:
        contents:
          suggested-value: false
    rally:
      keep_new_orders:
        contents:
          suggested-value: true
      terrain_speed:
        contents:
          suggested-value: true
      monks_fix:
        contents:
          suggested-value: true
      fight_on_the_way:
        contents:
          suggested-value: false
      follow_changes:
        contents:
          suggested-value: true
      run_when_aggressive:
        contents:
          suggested-value: false
      buttons:
        contents:
          suggested-value: true
    stance:
      button:
        contents:
          suggested-value: true
      start:
        contents:
          suggested-value: normal
    debug:
      log:
        contents:
          suggested-value: false
```

## improved-tunnelers 1.7.11

Dependencies are `framework ^3.0.7`, `frontend ^1.0.2`, `textResourceModifier ^0.3.0`, `map-extensions ^1.1.5`.

Hold activation until collapse damage and cadence are verified against vanilla. The module exposes numeric controls for both; these values are module defaults.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `denial` | `{"enabled": false, "sliderValue": 100}` | `{"enabled": true, "sliderValue": 100}` | Allow immediate repairs |
| `denial.message` | `false` | `true` | No denial to announce |
| `terrain.enabled` | `true` | `true` | Restore ground height |
| `retarget.enabled` | `false` | `true` | Keep single-target tunnels |
| `retarget.range` | `80` | `20` | Inactive with parent off |
| `retarget.max` | `10` | `10` | Inactive with parent off |
| `retarget.join_distance` | `15` | `15` | Inactive with parent off |
| `targets.towers_and_gates` | `false` | `true` | Keep original target classes |
| `targets.under_buildings` | `false` | `true` | Keep original route restrictions |
| `digging.unselectable` | `false` | `true` | Keep selection behavior |
| `digging.untargetable` | `false` | `true` | Keep combat vulnerability |
| `digging.trap_proof` | `false` | `true` | Keep trap vulnerability |
| `digging.overlay` | `false` | `true` | Keep original visibility |
| `collapse.damage` | `2500` | `1000` | Use module baseline pending parity |
| `collapse.spread` | `false` | `true` | Avoid nearby building damage |
| `collapse.entrance_lost` | `false` | `true` | Avoid additional collapse trigger |
| `collapse.tiles_per_second` | `80` | `10` | Use module baseline pending parity |
| `collapse.spread_radius` | `2` | `3` | Inactive with parent off |
| `collapse.spread_damage` | `60` | `56` | Inactive with parent off |
| `ui.enabled` | `false` | `true` | Keep original command set |
| `stances.enabled` | `false` | `true` | Keep original combat reactions |
| `raids.enabled` | `false` | `true` | Keep original raid makeup |
| `diagnostics.enabled` | `false` | `true` | Disable diagnostic logging |

```yaml
improved-tunnelers:
  config:
    denial:
      contents:
        suggested-value:
          enabled: false
          sliderValue: 100
      message:
        contents:
          suggested-value: false
    terrain:
      enabled:
        contents:
          suggested-value: true
    retarget:
      enabled:
        contents:
          suggested-value: false
      range:
        contents:
          suggested-value: 80
      max:
        contents:
          suggested-value: 10
      join_distance:
        contents:
          suggested-value: 15
    targets:
      towers_and_gates:
        contents:
          suggested-value: false
      under_buildings:
        contents:
          suggested-value: false
    digging:
      unselectable:
        contents:
          suggested-value: false
      untargetable:
        contents:
          suggested-value: false
      trap_proof:
        contents:
          suggested-value: false
      overlay:
        contents:
          suggested-value: false
    collapse:
      damage:
        contents:
          suggested-value: 2500
      spread:
        contents:
          suggested-value: false
      entrance_lost:
        contents:
          suggested-value: false
      tiles_per_second:
        contents:
          suggested-value: 80
      spread_radius:
        contents:
          suggested-value: 2
      spread_damage:
        contents:
          suggested-value: 60
    ui:
      enabled:
        contents:
          suggested-value: false
    stances:
      enabled:
        contents:
          suggested-value: false
    raids:
      enabled:
        contents:
          suggested-value: false
    diagnostics:
      enabled:
        contents:
          suggested-value: false
```

## custom-projectiles 1.8.21

Dependencies are `framework >=3.0.7`, `map-extensions ^1.0.0`, `gmResourceModifier ^0.3.1`, `protocol ^1.0.0`, `ui ^1.0.1`.

The installed definition credits Krarilotus. Included by request. Hold activation until the calendar needs a projectile configuration; an empty path supplies no unit overrides.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `projectile_config_file_selector` | `""` | `"ucp/plugins/Reconquista-*/resources/balance/reconquista-projectiles-1.8.6.yml"` | Use empty unit overrides |

```yaml
custom-projectiles:
  config:
    projectile_config_file_selector:
      contents:
        suggested-value: ''
```

## attack-move 1.0.2

Dependencies are `framework >=3.0.7`, `frontend >=1.0.2`.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `waypoints.always` | `true` | `true` | Make waypoints available |
| `waypoints.continue_move` | `true` | `true` | Resume queued movement |
| `stacking.alt` | `false` | `true` | Keep native stacking controls |

```yaml
attack-move:
  config:
    waypoints:
      always:
        contents:
          suggested-value: true
      continue_move:
        contents:
          suggested-value: true
    stacking:
      alt:
        contents:
          suggested-value: false
```

## outpost-control 1.0.17

Dependencies are `map-extensions ^1.0.0`, `framework >=3.0.7`, `frontend >=1.0.17`.

Hold activation until a scenario needs outpost changes. This profile keeps the optional gameplay features off.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `defenders.enabled` | `false` | `true` | Keep original defender controls |
| `defenders.walls` | `false` | `true` | Keep guard placement |
| `defenders.knights` | `false` | `true` | Keep knight guard behavior |
| `waves.exact` | `false` | `true` | Keep original wave scaling |
| `growth.enabled` | `false` | `true` | Keep wave sizes stable |
| `jobs.enabled` | `false` | `true` | Keep original wave orders |
| `jobs.slaves` | `50` | `50` | Inactive with parent off |
| `jobs.spearmen` | `50` | `50` | Inactive with parent off |
| `jobs.macemen` | `30` | `30` | Inactive with parent off |
| `jobs.swordsmen` | `60` | `60` | Inactive with parent off |
| `jobs.arab_swordsmen` | `50` | `50` | Inactive with parent off |
| `jobs.knights` | `40` | `40` | Inactive with parent off |
| `jobs.archers` | `30` | `30` | Inactive with parent off |
| `jobs.arab_archers` | `30` | `0` | Inactive with parent off |
| `jobs.slingers` | `30` | `30` | Inactive with parent off |
| `jobs.horse_archers` | `100` | `80` | Inactive with parent off |
| `jobs.fire_throwers` | `60` | `60` | Inactive with parent off |
| `siege.enabled` | `false` | `true` | Keep original siege behavior |
| `retarget.enabled` | `false` | `true` | Keep original target selection |
| `join.enabled` | `false` | `true` | Keep waves separate from AI armies |
| `diagnostics.log` | `false` | `true` | Disable diagnostic logging |

```yaml
outpost-control:
  config:
    defenders:
      enabled:
        contents:
          suggested-value: false
      walls:
        contents:
          suggested-value: false
      knights:
        contents:
          suggested-value: false
    waves:
      exact:
        contents:
          suggested-value: false
    growth:
      enabled:
        contents:
          suggested-value: false
    jobs:
      enabled:
        contents:
          suggested-value: false
      slaves:
        contents:
          suggested-value: 50
      spearmen:
        contents:
          suggested-value: 50
      macemen:
        contents:
          suggested-value: 30
      swordsmen:
        contents:
          suggested-value: 60
      arab_swordsmen:
        contents:
          suggested-value: 50
      knights:
        contents:
          suggested-value: 40
      archers:
        contents:
          suggested-value: 30
      arab_archers:
        contents:
          suggested-value: 30
      slingers:
        contents:
          suggested-value: 30
      horse_archers:
        contents:
          suggested-value: 100
      fire_throwers:
        contents:
          suggested-value: 60
    siege:
      enabled:
        contents:
          suggested-value: false
    retarget:
      enabled:
        contents:
          suggested-value: false
    join:
      enabled:
        contents:
          suggested-value: false
    diagnostics:
      log:
        contents:
          suggested-value: false
```

## build-over-workers 1.0.3

Dependencies are `framework ^3.0.7`, `frontend ^1.0.2`.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `buildings` | `true` | `true` | Avoid own-worker placement blocks |
| `walls` | `true` | `true` | Avoid own-worker wall blocks |
| `keepOnWalls` | `true` | `true` | Keep units on walls |
| `allies` | `false` | `true` | Preserve allied placement restrictions |

```yaml
build-over-workers:
  config:
    buildings:
      contents:
        suggested-value: true
    walls:
      contents:
        suggested-value: true
    keepOnWalls:
      contents:
        suggested-value: true
    allies:
      contents:
        suggested-value: false
```

## themed-buildings 1.0.4

Dependencies are `gmResourceModifier ^0.3.0`, `framework >=3.0.7`, `frontend >=1.0.2`.

Hold activation to preserve the Christmas texture stack.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `enabled` | `false` | `true` | Keep calendar building art |
| `preview` | `false` | `true` | Keep calendar placement art |
| `chapel` | `"european"` | `"european"` | Dormant art choice |
| `church` | `"arabian"` | `"arabian"` | Dormant art choice |
| `cathedral` | `"european"` | `"european"` | Dormant art choice |

```yaml
themed-buildings:
  config:
    enabled:
      contents:
        suggested-value: false
    preview:
      contents:
        suggested-value: false
    chapel:
      contents:
        suggested-value: european
    church:
      contents:
        suggested-value: arabian
    cathedral:
      contents:
        suggested-value: european
```

## autosave 1.0.1

Dependencies are `framework >=3.0.7`, `frontend >=1.0.2`, `textResourceModifier ^0.3.0`, `cffi ^1.0.0`.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `versions` | `5` | `5` | Keep five recovery points |
| `delete_after_days` | `7` | `7` | Keep seven-day restore window |

```yaml
autosave:
  config:
    versions:
      contents:
        suggested-value: 5
    delete_after_days:
      contents:
        suggested-value: 7
```

## ally-support 1.0.18

Check ally goods quantities against vanilla before activation. Loop prevention is part of the goods feature, which also exposes a sharing percentage.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `goods.enabled` | `true` | `true` | Keep ally goods requests |
| `goods.weak` | `false` | `true` | Keep original request thresholds |
| `goods.no_pingpong` | `true` | `true` | Prevent reciprocal request loops |
| `goods.useful` | `false` | `true` | Keep original goods priorities |
| `goods.protect` | `false` | `true` | Keep original donor reserves |
| `goods.rebuild` | `false` | `true` | Keep original rebuilding support |
| `goods.give_share` | `30` | `30` | Use module baseline pending parity |
| `gold.enabled` | `false` | `true` | Keep original gold support |
| `gold.ask` | `true` | `true` | Inactive with parent off |
| `gold.recruit` | `true` | `true` | Inactive with parent off |
| `gold.player` | `true` | `true` | Inactive with parent off |
| `gold.after_castle` | `true` | `true` | Inactive with parent off |
| `gold.recruit_buffer` | `300` | `300` | Inactive with parent off |
| `gold.keep` | `1000` | `1000` | Inactive with parent off |
| `gold.share` | `25` | `25` | Inactive with parent off |
| `help.enabled` | `false` | `true` | Keep original reinforcement behavior |
| `help.months` | `6` | `6` | Inactive with parent off |
| `help.recall` | `"strong"` | `"army"` | Inactive with parent off |
| `army.enabled` | `false` | `true` | Keep original army sharing |
| `army.share` | `75` | `75` | Inactive with parent off |
| `gates.enabled` | `false` | `true` | Keep original gate policy |
| `gates.keep` | `true` | `true` | Inactive with parent off |
| `diagnostics.log` | `false` | `true` | Disable diagnostic logging |

```yaml
ally-support:
  config:
    goods:
      enabled:
        contents:
          suggested-value: true
      weak:
        contents:
          suggested-value: false
      no_pingpong:
        contents:
          suggested-value: true
      useful:
        contents:
          suggested-value: false
      protect:
        contents:
          suggested-value: false
      rebuild:
        contents:
          suggested-value: false
      give_share:
        contents:
          suggested-value: 30
    gold:
      enabled:
        contents:
          suggested-value: false
      ask:
        contents:
          suggested-value: true
      recruit:
        contents:
          suggested-value: true
      player:
        contents:
          suggested-value: true
      after_castle:
        contents:
          suggested-value: true
      recruit_buffer:
        contents:
          suggested-value: 300
      keep:
        contents:
          suggested-value: 1000
      share:
        contents:
          suggested-value: 25
    help:
      enabled:
        contents:
          suggested-value: false
      months:
        contents:
          suggested-value: 6
      recall:
        contents:
          suggested-value: strong
    army:
      enabled:
        contents:
          suggested-value: false
      share:
        contents:
          suggested-value: 75
    gates:
      enabled:
        contents:
          suggested-value: false
      keep:
        contents:
          suggested-value: true
    diagnostics:
      log:
        contents:
          suggested-value: false
```

## lord-hunt 1.0.2

Hold activation. The exposed features change lord behavior or army priorities.

| Option | Vanilla-like value | Monsterfish value | Why |
| --- | --- | --- | --- |
| `hiding.enabled` | `false` | `true` | Keep original lord behavior |
| `hiding.siege` | `"hiding"` | `"hiding"` | Inactive with parent off |
| `hiding.split` | `50` | `50` | Inactive with parent off |
| `hiding.switch_alive` | `80` | `80` | Inactive with parent off |
| `hunt.enabled` | `false` | `true` | Keep original attack priorities |
| `hunt.share` | `50` | `50` | Inactive with parent off |
| `diagnostics.log` | `false` | `true` | Disable diagnostic logging |

```yaml
lord-hunt:
  config:
    hiding:
      enabled:
        contents:
          suggested-value: false
      siege:
        contents:
          suggested-value: hiding
      split:
        contents:
          suggested-value: 50
      switch_alive:
        contents:
          suggested-value: 80
    hunt:
      enabled:
        contents:
          suggested-value: false
      share:
        contents:
          suggested-value: 50
    diagnostics:
      log:
        contents:
          suggested-value: false
```
