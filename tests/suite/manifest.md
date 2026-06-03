# Test Suite Manifest

Total models: 30

## Short (5 models)

- `AdjP.inp`
- `BreakEnthalpy.inp`
- `CCTF_ColdLeg.inp`
- `ColdLegBreak.inp`
- `ColdLegBreakRst.inp`

## Short2 (5 models)

- `2hscase.1.old.inp`
- `AdjFlowLossTest1.inp`
- `AdjFlowLossTest2.inp`
- `AdjFlowLossTest3.inp`
- `AdjFlowLossTest4.inp`

## Valve (5 models)

- `1valv-SD-BC-Pcte.inp`
- `CBValve.inp`
- `CBValveCv.inp`
- `CBValveCvSJC.inp`
- `CBValveCv_Err4.inp`

## Pump (5 models)

- `PumpTorq2.inp`
  - #     pump motor torque test problem - IPMPTY = 3.
#     This test is identical to regression problem PumpTorq with
#     the added feature of the pump motor torque.  The pump motor
#     torque comes from control block id -680.
#
- `PumpTorq3.inp`
  - #     pump motor torque test problem - IPMPTY = 3.
#     This test is identical to PumpTorq2 with the added feature
#     that IPMPTR points to trip 1.  Initial motor torque will be
#     1000 N-m before trip and then 500 N-m after trip.
#
- `PumpTorq3R.inp`
  - #     pump motor torque test problem - IPMPTY = 3.
#     Restarts from PumpTorq3 at time zero.  If time zero restart
#     dump is good then PumpTorq3 and PumpTorq3R should be the same.
#
- `PumpTyp0.inp`
  - #    Simple pump IPMPTY = 0 test.  Closed loop with single PIPE component
#    connected to inlet and outlet of PUMP.  Pump trip is initially off
#    then goes on at 100 seconds.  Stays on to 300 seconds and then goes
#    off.  When trip is off the volumetric flow through the pump is
#    6.5 m^3/s and when the trip is on the volumetric flow through the pump is
#    7 m^3/s.
#
- `PumpTyp0_Rev1.inp`
  - #    Same as test problem PumpTyp0, except NPMPSD was changed from -1 to 2.
#    Signal variable 2 is trip status for trip 11.
#    Trip 11 is initially off, then goes on at 100 secs and then off again at 300 secs.
#

## Tee (5 models)

- `ptpL0.inp`
- `ptpL0a.inp`
- `ptpL0ar.inp`
- `ptpL0b.inp`
- `ptpL0br.inp`

## Contan (5 models)

- `CONTAN1.inp`
  - #    Base case for some CONTAN test problems.  This is a simple test problem with
#    a FILL-PIPE-BREAK.  It will be used to provide a mass and energy source and sink
#    for a CONTAN component.
#
- `CONTAN2.inp`
  - #    Same as test problem CONTAN1, except CONTAN component added.
#
- `CONTAN3.inp`
  - #    Same as test problem CONTAN2, except CONTAN RML was changed from 1.0 to 1000.
#
- `CONTAN4.inp`
  - #    Same as test problem CONTAN3, except region for BREAK 3 was changed from 0 to 2
#    and CONTAN ITRKL input was changed from 0 to 1.
#
- `CONTAN5.inp`
  - #    Same as test problem CONTAN4, except added legacycontm = .false. to namelist input
#    and added the addition input required for the CONTAN component.
#

