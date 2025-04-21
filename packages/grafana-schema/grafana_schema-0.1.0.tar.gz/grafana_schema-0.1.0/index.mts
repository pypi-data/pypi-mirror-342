import {
  Dashboard as CoreDashboard,
  Panel as CorePanel,
  RowPanel as CoreRowPanel,
} from "@grafana/schema";
import * as BarChartPanelCfg from "@grafana/schema/dist/esm/raw/composable/barchart/panelcfg/x/BarChartPanelCfg_types.gen";
import * as BarGaugePanelCfg from "@grafana/schema/dist/esm/raw/composable/bargauge/panelcfg/x/BarGaugePanelCfg_types.gen";
import * as GaugePanelCfg from "@grafana/schema/dist/esm/raw/composable/gauge/panelcfg/x/GaugePanelCfg_types.gen";
import * as PieChartPanelCfg from "@grafana/schema/dist/esm/raw/composable/piechart/panelcfg/x/PieChartPanelCfg_types.gen";
import * as StatPanelCfg from "@grafana/schema/dist/esm/raw/composable/stat/panelcfg/x/StatPanelCfg_types.gen";
import * as TablePanelCfg from "@grafana/schema/dist/esm/raw/composable/table/panelcfg/x/TablePanelCfg_types.gen";
import * as TimeSeriesPanelCfg from "@grafana/schema/dist/esm/raw/composable/timeseries/panelcfg/x/TimeSeriesPanelCfg_types.gen";

export interface BarGaugeOptions extends BarGaugePanelCfg.Options {}
export interface BarGauge extends Panel<BarGaugeOptions> {}

export interface BarChartOptions extends BarChartPanelCfg.Options {}
export interface BarChartPanelFieldConfig
  extends BarChartPanelCfg.FieldConfig {}
export interface BarChart
  extends Panel<BarChartOptions, BarChartPanelFieldConfig> {}

export interface GaugeOptions extends GaugePanelCfg.Options {}
export interface Gauge extends Panel<GaugeOptions> {}

export interface PieChartOptions extends PieChartPanelCfg.Options {}
export interface PieChartPanelFieldConfig
  extends PieChartPanelCfg.FieldConfig {}
export interface PieChart
  extends Panel<PieChartOptions, PieChartPanelFieldConfig> {}

export interface StatOptions extends StatPanelCfg.Options {}
export interface Stat extends Panel<StatOptions> {}

export interface TableOptions extends TablePanelCfg.Options {}
export interface TablePanelFieldConfig extends TablePanelCfg.FieldConfig {}
export interface Table extends Panel<TableOptions, TablePanelFieldConfig> {}

export interface TimeSeriesOptions extends TimeSeriesPanelCfg.Options {}
export interface TimeSeriesPanelFieldConfig
  extends TimeSeriesPanelCfg.FieldConfig {}
export interface TimeSeries
  extends Panel<TimeSeriesOptions, TimeSeriesPanelFieldConfig> {}

export type PluginPanel =
  | BarGauge
  | BarChart
  | Gauge
  | PieChart
  | Stat
  | Table
  | TimeSeries;

export interface Panel<
  TOptions = Record<string, unknown>,
  TCustomFieldConfig = Record<string, unknown>
> extends Omit<CorePanel<TOptions, TCustomFieldConfig>, "options"> {
  options?: TOptions;
}
export interface RowPanel extends Omit<CoreRowPanel, "panels"> {
  panels: PluginPanel[];
}

export interface Dashboard extends Omit<CoreDashboard, "panels"> {
  panels: Array<PluginPanel | RowPanel>;
}
