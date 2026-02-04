import React, { useState, useEffect } from 'react';
import { Zap, ShoppingCart } from 'lucide-react';

const USER_SEGMENT = Math.random() > 0.5 ? 'B' : 'A';

const getColorByStock = (stock) => {
  if (stock >= 20) return 'bg-emerald-500/20 border-emerald-500 text-emerald-400';
  if (stock >= 10) return 'bg-lime-400/20 border-lime-400 text-lime-300';
  if (stock >= 5)  return 'bg-orange-500/20 border-orange-500 text-orange-400';
  return 'bg-rose-600/20 border-rose-600 text-rose-400 shadow-[0_0_15px_rgba(225,29,72,0.3)] animate-pulse';
};

export default function App() {
  const [data, setData] = useState({ root: null, nodes: [] });
  const [loading, setLoading] = useState(true);
  const [viewState, setViewState] = useState({ x: 0, y: 0, zoom: 0.8 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  
  // Ez figyeli, melyik kategória felett van az egér
  const [hoveredNodeId, setHoveredNodeId] = useState(null);

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
        // Bővített fallback adatok a kérésed alapján
        setData({
          root: { id: 'root', label: 'Raktár', type: 'category', x: 0, y: 0 },
          nodes: [
            { id: 'pc', label: 'Számítógép alkatrészek', type: 'category', x: -300, y: 0, parent: 'root' },
            { id: 'vga', label: 'VGA', type: 'subcategory', x: -600, y: -150, parent: 'pc' },
            { id: 'psu', label: 'Táp', type: 'subcategory', x: -600, y: 150, parent: 'pc' },
            // Termékek (csak ha a szülő hoverelve van)
            { id: 'p1', label: 'RTX 4090', type: 'product', price: '750.000 Ft', stock: 3, x: -900, y: -250, parent: 'vga', img: 'https://placehold.co/200x150/0f172a/3b82f6?text=RTX+4090' },
            { id: 'p2', label: 'RX 7900 XTX', type: 'product', price: '420.000 Ft', stock: 12, x: -900, y: -50, parent: 'vga', img: 'https://placehold.co/200x150/0f172a/3b82f6?text=RX+7900' },
            { id: 'p3', label: '1000W Gold PSU', type: 'product', price: '65.000 Ft', stock: 25, x: -900, y: 150, parent: 'psu', img: 'https://placehold.co/200x150/0f172a/3b82f6?text=PSU+1000W' }
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

  if (loading) return <div className="h-screen bg-[#050507] flex items-center justify-center text-blue-500 font-mono tracking-tighter">INITIALIZING_TORMENT_V1.0...</div>;

  return (
    <div className="w-full h-screen bg-[#050507] text-white flex flex-col overflow-hidden select-none"
         onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={() => setIsDragging(false)}
         onWheel={(e) => setViewState(v => ({...v, zoom: Math.min(Math.max(v.zoom - e.deltaY * 0.001, 0.2), 2)}))}>
      
      <nav className="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-black/40 backdrop-blur-md z-50">
        <div className="flex items-center gap-2"><Zap className="text-blue-500" /> <span className="font-black tracking-widest">TORMENT OS</span></div>
        <div className="flex items-center gap-6 opacity-60 text-xs font-mono">
          <span>COORDS: {Math.round(viewState.x)}:{Math.round(viewState.y)}</span>
          <span>SEGMENT: {USER_SEGMENT}</span>
          <ShoppingCart className="w-5 h-5 cursor-pointer hover:text-blue-400 transition-colors" />
        </div>
      </nav>

      <div className="flex-1 relative cursor-grab active:cursor-grabbing">
        <div className="absolute inset-0 transition-transform duration-75"
             style={{ transform: `translate(${viewState.x}px, ${viewState.y}px) scale(${viewState.zoom})`, transformOrigin: 'center' }}>
          
          <svg className="absolute inset-[-5000px] w-[10000px] h-[10000px] pointer-events-none">
            {data.nodes.map(node => {
              const p = node.parent === 'root' ? data.root : data.nodes.find(n => n.id === node.parent);
              // Csak akkor rajzolunk vonalat, ha a célpont látható
              const isVisible = node.type !== 'product' || hoveredNodeId === node.parent;
              return p && isVisible && (
                <line key={node.id} x1={p.x+5000} y1={p.y+5000} x2={node.x+5000} y2={node.y+5000} 
                      stroke={node.type === 'product' ? '#3b82f644' : '#1e293b'} strokeWidth="2" strokeDasharray={node.type === 'product' ? "5,5" : "0"} />
              );
            })}
          </svg>

          {[data.root, ...data.nodes].map(node => {
            const isVisible = node.type !== 'product' || hoveredNodeId === node.parent;
            if (!isVisible) return null;

            return (
              <div 
                key={node.id} 
                onMouseEnter={() => node.type !== 'product' && setHoveredNodeId(node.id)}
                className={`absolute transition-all duration-300 border-2 
                  ${node.type === 'product' 
                    ? `w-56 bg-slate-900/90 backdrop-blur-sm rounded-xl overflow-hidden -ml-28 -mt-32 p-0 ${getColorByStock(node.stock)}` 
                    : 'w-48 h-16 bg-slate-900 border-blue-600 rounded-full flex items-center justify-center -ml-24 -mt-8'
                  }`}
                style={{ left: node.x+5000, top: node.y+5000 }}>
                
                {node.type === 'product' ? (
                  <div className="flex flex-col">
                    <img src={node.img} alt="" className="w-full h-28 object-cover border-b border-white/10" />
                    <div className="p-3">
                      <div className="text-xs font-black truncate mb-1">{node.label}</div>
                      <div className="text-blue-400 font-mono text-sm">{node.price}</div>
                      <div className="mt-2 text-[9px] uppercase tracking-tighter opacity-70">Stock Level: {node.stock} units</div>
                    </div>
                  </div>
                ) : (
                  <span className="text-xs font-bold uppercase tracking-widest text-center px-4">{node.label}</span>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}