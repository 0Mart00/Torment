import React, { useState, useEffect, useMemo, useRef } from 'react';
import { Zap, Search, User, ShoppingCart, Info, MousePointer2, Move } from 'lucide-react';

const USER_SEGMENT = Math.random() > 0.5 ? 'B' : 'A';

const getColorByStock = (stock) => {
  if (stock >= 20) return 'bg-emerald-500 border-emerald-300';
  if (stock >= 10) return 'bg-lime-400 border-lime-200';
  if (stock >= 5)  return 'bg-orange-500 border-orange-300';
  return 'bg-rose-600 border-rose-400 shadow-[0_0_20px_rgba(225,29,72,0.4)] animate-pulse';
};

export default function App() {
  const [data, setData] = useState({ root: null, nodes: [] });
  const [loading, setLoading] = useState(true);
  const [viewState, setViewState] = useState({ x: 0, y: 0, zoom: 0.8 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const loadGraph = async () => {
      try {
        const res = await fetch('/api/catalog/mindmap/');
        if (!res.ok) throw new Error();
        const json = await res.json();
        setData({
          root: json.nodes.find(n => n.id === 'root'),
          nodes: json.nodes.filter(n => n.id !== 'root')
        });
      } catch (err) {
        // Fallback adatok fejlesztéshez
        setData({
          root: { id: 'root', label: 'Mag', type: 'category', x: 0, y: 0 },
          nodes: [
            { id: 'c1', label: 'Szoftver', type: 'category', x: -250, y: 150, parent: 'root' },
            { id: 'p1', label: 'Neural Link', type: 'product', price: 499, stock: 4, x: -350, y: 350, parent: 'c1' }
          ]
        });
      } finally {
        setLoading(false);
      }
    };
    loadGraph();
  }, []);

  const handleMouseDown = (e) => {
    if (e.button !== 0) return;
    setIsDragging(true);
    setDragStart({ x: e.clientX - viewState.x, y: e.clientY - viewState.y });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setViewState(prev => ({ ...prev, x: e.clientX - dragStart.x, y: e.clientY - dragStart.y }));
  };

  if (loading) return <div className="h-screen bg-[#050507] flex items-center justify-center text-blue-500 font-mono">LOADING_SYSTEM...</div>;

  return (
    <div className="w-full h-screen bg-[#050507] text-white flex flex-col overflow-hidden select-none"
         onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={() => setIsDragging(false)}
         onWheel={(e) => setViewState(v => ({...v, zoom: Math.min(Math.max(v.zoom - e.deltaY * 0.001, 0.3), 2)}))}>
      
      <nav className="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-black/40 backdrop-blur-md z-50">
        <div className="flex items-center gap-2"><Zap className="text-blue-500" /> <span className="font-black tracking-widest">TORMENT OS</span></div>
        <div className="flex items-center gap-6 opacity-60 text-xs">
          <span>SEGMENT: {USER_SEGMENT}</span>
          <ShoppingCart className="w-5 h-5" />
        </div>
      </nav>

      <div className="flex-1 relative cursor-grab active:cursor-grabbing">
        <div className="absolute inset-0 transition-transform duration-75"
             style={{ transform: `translate(${viewState.x}px, ${viewState.y}px) scale(${viewState.zoom})`, transformOrigin: 'center' }}>
          
          <svg className="absolute inset-[-5000px] w-[10000px] h-[10000px]">
            {data.nodes.map(node => {
              const p = node.parent === 'root' ? data.root : data.nodes.find(n => n.id === node.parent);
              return p && <line key={node.id} x1={p.x+5000} y1={p.y+5000} x2={node.x+5000} y2={node.y+5000} stroke="#1e293b" strokeWidth="2" />;
            })}
          </svg>

          {[data.root, ...data.nodes].map(node => (
            <div key={node.id} className={`absolute rounded-full border-2 flex items-center justify-center transition-all
              ${node.type === 'product' ? getColorByStock(node.stock) : 'bg-slate-900 border-blue-600'}
              ${viewState.zoom > 0.6 ? 'w-40 h-40 -ml-20 -mt-20' : 'w-10 h-10 -ml-5 -mt-5'}`}
              style={{ left: node.x+5000, top: node.y+5000 }}>
              <span className="text-[10px] font-bold uppercase text-center px-2">{node.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}