from app.engine.signal_fusion import FusionMetrics
from app.engine.trading_state import TradingStateStore, trade_record_from_paper


def test_build_report_structure():
    store = TradingStateStore(capital_inicial=10000, capital_actual=10050, iterations=5)
    trades = {
        "BTCUSDT": [
            trade_record_from_paper(
                trade_id=1,
                symbol="BTCUSDT",
                action="buy",
                entry_price=100.0,
                exit_price=101.0,
                quantity=0.01,
                profit_loss=0.5,
                fusion=FusionMetrics(combined=10.0, ild=1.0, egm=0.5, rol=0.2, pio=0.3, ogm=0.1),
            )
        ]
    }
    report = store.build_report(trades)
    assert "metadata" in report
    assert "summary" in report
    assert "by_symbol" in report
    assert "trades" in report
    assert "events" in report
    assert report["metadata"]["iterations"] == 5
    assert report["summary"]["net_profit"] == 0.5
    assert report["trades"]["BTCUSDT"][0]["combined"] == 10.0


def test_trade_record_has_nertzh_fields():
    record = trade_record_from_paper(
        trade_id=1,
        symbol="BTCUSDT",
        action="buy",
        entry_price=91000,
        exit_price=91050,
        quantity=0.002,
        profit_loss=0.1,
        tp_price=91600,
        sl_price=90800,
    )
    assert record["order_id"].startswith("paper-")
    assert record["outcome_status"] == "final"
    assert record["risk_reward_ratio"] == 3.0
    assert record["tp_price"] == 91600