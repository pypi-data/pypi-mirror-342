import random
from typing import List
import networkx as nx
from .agent import Agent


class AgentNetwork:
    def __init__(self, 
                 agents: List[Agent],
                 network_type: str = "BA", 
                 m: int = 2,
                 k_smallworld: int = 4,
                 p_smallworld: float = 0.1,
                 p_er: float = 0.01,
                 seed: int = 42):
        """
        Args:
            agents: Agentのリスト
            network_type: "BA" / "WS" / "ER"
            m: BAモデルで新規ノードが接続するエッジ数
            k_smallworld: WSモデルで各ノードが接続する近傍ノード数(偶数)
            p_smallworld: WSモデルでエッジをランダムに再接続する確率
            p_er: ERモデルでエッジを接続する確率
            seed: 乱数シード
        """
        self.graph = nx.Graph()
        self.agents = {agent.agent_id: agent for agent in agents}
        self.similarity_threshold = 0.5
        self.trust_threshold = 0.5
        self.network_type = network_type
        self.m = m
        self.k_smallworld = k_smallworld
        self.p_smallworld = p_smallworld
        self.p_er = p_er
        self.seed = seed
        
        self._create_ba_network()
    
    def _create_ba_network(self):
        num_agents = len(self.agents)
        if self.network_type == "BA":
            if num_agents < self.m:
                raise ValueError("Agentの数はmより大きくする必要があります。")
            base_graph = nx.barabasi_albert_graph(n=num_agents, m=self.m, seed=self.seed)
        
        elif self.network_type == "WS":
            base_graph = nx.watts_strogatz_graph(n=num_agents, 
                                                 k=self.k_smallworld, 
                                                 p=self.p_smallworld, 
                                                 seed=self.seed)
        
        elif self.network_type == "ER":
            base_graph = nx.erdos_renyi_graph(n=num_agents, p=self.p_er, seed=self.seed)
        
        else:
            raise ValueError("network_typeは'BA', 'WS', 'ER'のいずれかを指定してください。")
        
        # エージェントIDのリストを取得
        agent_ids = list(self.agents.keys())
        
        # GraphノードをエージェントIDに再ラベル
        mapping = {node: agent_id for node, agent_id in zip(base_graph.nodes(), agent_ids)}
        base_graph = nx.relabel_nodes(base_graph, mapping)
        
        # エージェントをネットワークに追加
        for agent_id, agent in self.agents.items():
            self.graph.add_node(agent_id, agent=agent)
        
        # エッジを追加
        for (n1, n2) in base_graph.edges():
            edge_weight = random.uniform(0, 1)
            self.graph.add_edge(n1, n2, weight=edge_weight)
    
    def get_agent(self, agent_id: int) -> Agent:
        """
        エージェントIDからエージェントを取得。
        """
        return self.agents.get(agent_id)
    
    def get_neighbor_agents(self, agent_id: int) -> List[Agent]:
        """
        エージェントIDの隣接エージェントのリストを取得。
        """
        # 隣接エージェントのIDを取得
        neighbor_ids = self.graph.neighbors(agent_id)
        # 隣接エージェントをインスタンス化
        neighbor_agents = [self.get_agent(id) for id in neighbor_ids]
        return neighbor_agents
    
    def update_edge_weight(self, agent1_id: int, agent2_id: int):
        """
        2つのエージェント間のエッジの重みを更新。
        """
        self.graph[agent1_id][agent2_id]["weight"] += 0.1
    
    # 下記はいらないかも
    
    
    def calc_field_similarity(self, agent1: Agent, agent2: Agent):
        """
        エージェント間のフィールド類似度を計算。
        """
        return len(set(agent1.data_types).intersection(set(agent2.data_types)))
    
    def calc_average_trust(self, agent1: Agent, agent2: Agent):
        """
        2つのエージェントの信頼スコアの平均を計算。
        """
        return (agent1.trust_score + agent2.trust_score) / 2
    
    def add_agent(self, agent: Agent):
        """
        ネットワークにエージェントを追加。
        """
        self.graph.add_node(agent.agent_id, agent=agent)
        self.agents[agent.agent_id] = agent
        self.connect_agent(agent)
    
    def connect_agent(self, new_agent: Agent):
        """
        新しいエージェントを他のエージェントと接続。
        """
        potential_connections = []
        
        for agent_id, existing_agent in self.agents.items():
            if agent_id == new_agent.agent_id:
                continue  # 自分自身とは接続しない
            
            similarity = self.calc_field_similarity(new_agent, existing_agent)
            average_trust = self.calc_average_trust(new_agent, existing_agent)
            
            if similarity >= self.similarity_threshold and average_trust >= self.trust_threshold:
                combined_weight = similarity * average_trust
                potential_connections.append((agent_id, combined_weight))
        
        # 類似度と信頼スコアに基づいてソート
        potential_connections.sort(key=lambda x: x[1], reverse=True)
        
        # 上位N件を接続対象とする
        top_n = 5  # 接続するエージェントの最大数
        connections_made = 0
        
        for agent_id, weight in potential_connections:
            if not self.graph.has_edge(new_agent.agent_id, agent_id):
                self.graph.add_edge(new_agent.agent_id, agent_id, weight=weight)
                connections_made += 1
                if connections_made >= top_n:
                    break