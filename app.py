# !pip install pandas
# !pip install dash dash-bootstrap-components plotly pandas
# !python app.py

import pandas as pd
import random
from dash import Dash, dcc, html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# 대시보드 초기 설정
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# 샘플 데이터 생성
time_slots = [f"{i}:00" for i in range(8, 23)]  # 08:00 ~ 22:00 시간대
sections = ['무주읍 ↔ 설천면', '설천면 ↔ 무풍면', '무풍면 ↔ 무주읍']
current_congestion_level = random.randint(50, 100)  # 현재 혼잡도 지수

# 혼잡도 예측 데이터 프레임
congestion_data = pd.DataFrame({
    '시간대': time_slots,
    '혼잡도': [random.randint(30, 100) for _ in time_slots],
})

# 대시보드 레이아웃
app.layout = dbc.Container([
    # 1. 대시보드 제목
    html.H2("혼잡도 관리 대시보드", className="text-center text-primary mb-4"),

    # 상단: 매출, 혼잡도 지수, 혼잡 구간 경고
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("오늘의 매출", className="card-title"),
                    html.H3("$5k", className="card-text text-success"),
                    html.P("10% from yesterday", className="text-muted"),
                ])
            ], color="dark", outline=True, className="mb-3"),

            dbc.Card([
                dbc.CardBody([
                    html.H5("전체 혼잡도 지수", className="card-title"),
                    html.H3(f"{current_congestion_level}%", className="card-text text-danger"),
                    html.P("5% from yesterday", className="text-muted"),
                ])
            ], color="dark", outline=True, className="mb-3"),

            dbc.Card([
                dbc.CardBody([
                    html.H5("주요 혼잡 구간 경고", className="card-title"),
                    html.Ul([html.Li(f"{section} - 혼잡도 초과", className="text-danger") for section in sections]),
                ])
            ], color="dark", outline=True, className="mb-3"),
        ], width=3),

        # 오른쪽 상단: 실시간 방문객 수 분포와 무주군 혼잡도 지도
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("실시간 방문객 수 및 분포", className="card-title"),
                    dcc.Graph(
                        id='visitor_distribution',
                        config={'displayModeBar': False},
                        figure=go.Figure(data=[
                            go.Pie(labels=['무주읍', '설천면', '무풍면'], values=[300, 200, 150], hole=0.3)
                        ]).update_layout(margin=dict(t=0, b=0, l=0, r=0), height=200)  # 높이를 절반으로 설정
                    ),
                ])
            ], color="dark", outline=True, className="mb-3"),

            dbc.Card([
                dbc.CardBody([
                    html.H5("무주군 혼잡도 지도", className="card-title"),
                    dcc.Graph(
                        id="congestion_map",
                        config={'displayModeBar': False},
                        figure=go.Figure(
                            go.Scattermapbox(
                                lat=[36.007, 35.969, 35.957, 36.053, 35.941, 35.910],
                                lon=[127.660, 127.667, 127.680, 127.704, 127.640, 127.628],
                                mode="markers+text",
                                marker=dict(
                                    size=14,
                                    color=['green', 'yellow', 'red', 'green', 'red', 'yellow'],
                                    opacity=0.7
                                ),
                                text=['무주읍', '설천면', '무풍면', '적상면', '안성면', '부남면'],
                                textposition="top center"
                            )
                        ).update_layout(
                            mapbox=dict(
                                style="carto-positron",
                                zoom=10,
                                center={"lat": 36.0, "lon": 127.66}
                            ),
                            margin=dict(t=0, b=0, l=0, r=0),
                            height=250  # 지도의 높이를 절반으로 설정
                        )
                    ),
                ])
            ], color="dark", outline=True),
        ], width=9),
    ], className="mb-4"),

    # 하단: 혼잡도 변화 차트와 구간별 혼잡도 비교 차트
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("혼잡도 변화 차트", className="card-title"),
                dcc.Graph(
                    id="congestion_chart",
                    config={'displayModeBar': False},
                    figure=go.Figure(
                        data=go.Scatter(x=congestion_data['시간대'], y=congestion_data['혼잡도'], mode='lines+markers',
                                        line=dict(color='firebrick'))
                    ).update_layout(title="시간대별 혼잡도 예측", margin=dict(t=50))
                ),
            ])
        ], color="dark", outline=True), width=6),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("구간별 혼잡도 비교 차트", className="card-title"),
                dcc.Graph(
                    id="comparison_chart",
                    config={'displayModeBar': False},
                    figure=go.Figure(
                        data=[
                            go.Bar(name="무주읍 ↔ 설천면", x=time_slots, y=[random.randint(40, 90) for _ in time_slots]),
                            go.Bar(name="설천면 ↔ 무풍면", x=time_slots, y=[random.randint(30, 80) for _ in time_slots]),
                        ]
                    ).update_layout(barmode='group', title="구간별 혼잡도 비교", margin=dict(t=50))
                ),
            ])
        ], color="dark", outline=True), width=6),
    ])
])

# 대시보드 실행

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=9090, debug=True)




