# SNAP-MCP Test Report

Models tested: 30

## Summary

| Phase | Passed | Failed |
|---|---|---|
| Import (ASCII → SNAP) | 30 | 0 |
| Save (.med) | 30 | 0 |
| Re-open (.med) | 30 | 0 |
| **End-to-end** | **30** | **0** |

## Results by Suite

### Contan

| Model | Import | Save | Re-open | Components | Notes |
|---|---|---|---|---|---|
| [CONTAN1.inp](suite/Contan/CONTAN1.inp) | ✓ | ✓ | ✓ | 5 |  |
| [CONTAN2.inp](suite/Contan/CONTAN2.inp) | ✓ | ✓ | ✓ | 6 |  |
| [CONTAN3.inp](suite/Contan/CONTAN3.inp) | ✓ | ✓ | ✓ | 10 |  |
| [CONTAN4.inp](suite/Contan/CONTAN4.inp) | ✓ | ✓ | ✓ | 10 |  |
| [CONTAN5.inp](suite/Contan/CONTAN5.inp) | ✓ | ✓ | ✓ | 10 |  |

### Pump

| Model | Import | Save | Re-open | Components | Notes |
|---|---|---|---|---|---|
| [PumpTorq2.inp](suite/Pump/PumpTorq2.inp) | ✓ | ✓ | ✓ | 8 |  |
| [PumpTorq3.inp](suite/Pump/PumpTorq3.inp) | ✓ | ✓ | ✓ | 8 |  |
| [PumpTorq3R.inp](suite/Pump/PumpTorq3R.inp) | ✓ | ✓ | ✓ | 0 |  |
| [PumpTyp0.inp](suite/Pump/PumpTyp0.inp) | ✓ | ✓ | ✓ | 5 |  |
| [PumpTyp0_Rev1.inp](suite/Pump/PumpTyp0_Rev1.inp) | ✓ | ✓ | ✓ | 6 |  |

### Short

| Model | Import | Save | Re-open | Components | Notes |
|---|---|---|---|---|---|
| [AdjP.inp](suite/Short/AdjP.inp) | ✓ | ✓ | ✓ | 4 |  |
| [BreakEnthalpy.inp](suite/Short/BreakEnthalpy.inp) | ✓ | ✓ | ✓ | 6 |  |
| [CCTF_ColdLeg.inp](suite/Short/CCTF_ColdLeg.inp) | ✓ | ✓ | ✓ | 5 |  |
| [ColdLegBreak.inp](suite/Short/ColdLegBreak.inp) | ✓ | ✓ | ✓ | 6 |  |
| [ColdLegBreakRst.inp](suite/Short/ColdLegBreakRst.inp) | ✓ | ✓ | ✓ | 0 |  |

### Short2

| Model | Import | Save | Re-open | Components | Notes |
|---|---|---|---|---|---|
| [2hscase.1.old.inp](suite/Short2/2hscase.1.old.inp) | ✓ | ✓ | ✓ | 10 |  |
| [AdjFlowLossTest1.inp](suite/Short2/AdjFlowLossTest1.inp) | ✓ | ✓ | ✓ | 4740 |  |
| [AdjFlowLossTest2.inp](suite/Short2/AdjFlowLossTest2.inp) | ✓ | ✓ | ✓ | 324 |  |
| [AdjFlowLossTest3.inp](suite/Short2/AdjFlowLossTest3.inp) | ✓ | ✓ | ✓ | 324 |  |
| [AdjFlowLossTest4.inp](suite/Short2/AdjFlowLossTest4.inp) | ✓ | ✓ | ✓ | 324 |  |

### Tee

| Model | Import | Save | Re-open | Components | Notes |
|---|---|---|---|---|---|
| [ptpL0.inp](suite/Tee/ptpL0.inp) | ✓ | ✓ | ✓ | 6 |  |
| [ptpL0a.inp](suite/Tee/ptpL0a.inp) | ✓ | ✓ | ✓ | 6 |  |
| [ptpL0ar.inp](suite/Tee/ptpL0ar.inp) | ✓ | ✓ | ✓ | 6 |  |
| [ptpL0b.inp](suite/Tee/ptpL0b.inp) | ✓ | ✓ | ✓ | 6 |  |
| [ptpL0br.inp](suite/Tee/ptpL0br.inp) | ✓ | ✓ | ✓ | 6 |  |

### Valve

| Model | Import | Save | Re-open | Components | Notes |
|---|---|---|---|---|---|
| [1valv-SD-BC-Pcte.inp](suite/Valve/1valv-SD-BC-Pcte.inp) | ✓ | ✓ | ✓ | 4 |  |
| [CBValve.inp](suite/Valve/CBValve.inp) | ✓ | ✓ | ✓ | 6 |  |
| [CBValveCv.inp](suite/Valve/CBValveCv.inp) | ✓ | ✓ | ✓ | 6 |  |
| [CBValveCvSJC.inp](suite/Valve/CBValveCvSJC.inp) | ✓ | ✓ | ✓ | 8 |  |
| [CBValveCv_Err4.inp](suite/Valve/CBValveCv_Err4.inp) | ✓ | ✓ | ✓ | 6 |  |

## Component Type Coverage

| Component Type | Total instances across test suite |
|---|---|
| CONTROL_BLOCK | 4810 |
| SIGNAL_VARIABLE | 889 |
| BREAK | 35 |
| HEAT_STRUCTURE | 29 |
| PIPE | 28 |
| POWER | 27 |
| FILL | 20 |
| TRIP | 11 |
| TEE | 6 |
| VALVE | 5 |
| CONTAN_COMPARTMENT | 4 |
| PUMP | 4 |
| VESSEL | 3 |

## Prompt Files

Reconstruction prompts are saved alongside summaries in `tests/results/`.
Each prompt is a self-contained instruction for an AI using the snap-trace MCP to recreate the model.
