import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import gaussian_kde

# plot for simple backtest from analyzer class
class PlotBacktest:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.pf = analyzer.pf
        self.ss = analyzer.ss

    def plot_backtest(
        self,
        title: str = "Backtest Results",
        export_html: bool = False,
        export_image: bool = False,
        file_name: str = "backtest_plot",
    ) -> go.Figure:
        strategy_equity = self.pf.value()
        try:
            benchmark_equity = self.pf.benchmark_value()
        except AttributeError:
            benchmark_equity = pd.Series(index=strategy_equity.index, dtype=float)

        strat_dd = (
            (strategy_equity - strategy_equity.cummax()) / strategy_equity.cummax() * 100
        )
        bench_dd = (
            (benchmark_equity - benchmark_equity.cummax()) / benchmark_equity.cummax() * 100
            if not benchmark_equity.empty
            else pd.Series(index=strategy_equity.index, dtype=float)
        )

        rets = self.pf.returns()

        trades = self.pf.trades.records_readable
        entries = trades["Entry Timestamp"].astype("int64")
        exits = trades["Exit Timestamp"].fillna(strategy_equity.index[-1]).astype("int64")
        idx_int = rets.index.astype("int64").values
        open_trades = (
            (idx_int[:, None] >= entries.values) & (idx_int[:, None] <= exits.values)
        ).any(axis=1)
        rets = rets[open_trades]

        factor_root = self.ss._annual_factor(self.analyzer.timeframe, root=True)
        factor = self.ss._annual_factor(self.analyzer.timeframe, root=False)
        window = max(1, int(factor / 4))
        window_label = "90-days"

        strat_mean = rets.rolling(window, min_periods=window).mean()
        strat_std = rets.rolling(window, min_periods=window).std(ddof=1)
        rolling_sharpe = (strat_mean / strat_std) * factor_root

        try:
            bench_rets = self.pf.benchmark_returns()
            bench_mean = bench_rets.rolling(window, min_periods=window).mean()
            bench_std = bench_rets.rolling(window, min_periods=window).std(ddof=1)
            rolling_bench_sharpe = (bench_mean / bench_std) * factor_root
        except AttributeError:
            rolling_bench_sharpe = pd.Series(index=rolling_sharpe.index, dtype=float)

        rolling_sharpe = rolling_sharpe.iloc[window:]
        rolling_bench_sharpe = rolling_bench_sharpe.iloc[window:]

        if "Return [%]" in trades.columns:
            trade_returns = (
                trades["Return [%]"].astype(str).str.rstrip("% ").astype(float)
            )
        else:
            trade_returns = trades["Return"].dropna() * 100

        kde = gaussian_kde(trade_returns.values, bw_method="scott")
        x_kde = np.linspace(trade_returns.min(), trade_returns.max(), 200)
        y_kde = kde(x_kde) * 100

        fig = make_subplots(
            rows=2,
            cols=2,
            shared_xaxes=False,
            vertical_spacing=0.05,
            horizontal_spacing=0.1,
            row_heights=[0.5, 0.5],
            column_widths=[0.7, 0.3],
            subplot_titles=[
                "Equity Curve",
                "Rolling Sharpe",
                "Drawdown Curve",
                "Trade Returns Distribution",
            ],
        )

        fig.add_trace(
            go.Scatter(
                x=strategy_equity.index,
                y=strategy_equity.values,
                mode="lines",
                name="Strategy Equity",
                fill="tozeroy",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=benchmark_equity.index,
                y=benchmark_equity.values,
                mode="lines",
                name="Benchmark Equity",
                fill="tozeroy",
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=rolling_sharpe.index,
                y=rolling_sharpe.values,
                mode="lines",
                name=f"Rolling Sharpe (Strategy) ({window_label})",
            ),
            row=1,
            col=2,
        )
        fig.add_trace(
            go.Scatter(
                x=rolling_bench_sharpe.index,
                y=rolling_bench_sharpe.values,
                mode="lines",
                name=f"Rolling Sharpe (Benchmark) ({window_label})",
            ),
            row=1,
            col=2,
        )
        fig.add_hline(y=0, line=dict(color="white", dash="dash", width=2), row=1, col=2)

        fig.add_trace(
            go.Scatter(
                x=strategy_equity.index,
                y=strat_dd.values,
                mode="lines",
                name="Strategy Drawdown",
                fill="tozeroy",
            ),
            row=2,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=benchmark_equity.index,
                y=bench_dd.values,
                mode="lines",
                name="Benchmark Drawdown",
                fill="tozeroy",
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Histogram(
                x=trade_returns,
                nbinsx=30,
                histnorm="percent",
                name="Return Histogram",
                showlegend=False,
            ),
            row=2,
            col=2,
        )
        fig.add_trace(
            go.Scatter(x=x_kde, y=y_kde, mode="lines", name="KDE (%)"),
            row=2,
            col=2,
        )
        fig.add_vline(x=0, line=dict(color="white", dash="dash", width=2), row=2, col=2)

        fig.update_layout(
            title=title, hovermode="x unified", template="plotly_dark", height=700
        )
        fig.update_xaxes(rangeslider_visible=False, row=1, col=1)
        fig.update_xaxes(title_text="Returns [%]", row=2, col=2)

        if export_html:
            fig.write_html(f"{file_name}.html")
        if export_image:
            try:
                fig.write_image(f"{file_name}.png")
            except ValueError:
                pass

        return fig

# plot for oos backtest from optimizer class
