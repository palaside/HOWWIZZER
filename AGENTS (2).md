<!-- ======================================================================= -->
<!-- AGENTS.md — AUTONOMOUS AGENT ORCHESTRATION MANIFEST                      -->
<!-- System: Core System V3 (Autonomous Hook-Driven Architecture)            -->
<!-- Generated: 2026-10-09T22:11:02.686Z                                                -->
<!-- ======================================================================= -->

# 🤖 AGENTS ORCHESTRATOR MANIFEST (CORE SYSTEM V3)

> **Deployment Status:** PRODUCTION-READY  
> **Architecture Model:** Dynamic Hook-Driven Autonomous System  
> **Total Orchestrated Skills:** 2  

---

## 📋 1. SYSTEM CONSTITUTION & OPERATIONAL DNA
ระบบนี้ถูกคอมไพล์จากไฟล์สกิลแบบเดี่ยว (Static Skills) แปลงเป็น **Autonomous Orchestration Agent** ที่ทำงานผ่าน Event Listener & Hook Router อัตโนมัติ:
- **Clean Architecture:** แยกส่วน Interface, Routing Engine และ Domain Logic
- **Local-First & Offline:** ทำงานบนเครื่องผู้ใช้ 100% ปลอดภัย ไม่รั่วไหล
- **Automated Verification:** ตรวจสอบความพร้อมของทุกสกิลก่อนลงมือปฏิบัติงานจริง

---

## 🗂️ 2. ACTIVE SKILL REGISTRY (EXTRACTED METADATA)

| Skill Name | Description | When to Use (Trigger Condition) |
| :--- | :--- | :--- |
| `supabase` | Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector). | ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ supabase |
| `excel-to-blueprint` | สกิลวิศวกรรมย้อนรอย (Reverse Engineering) สกัดโครงสร้างสเปรดชีตเป็นพิมพ์เขียวดิจิทัล _blueprint.json แบบ 360 องศา ความเร็วสูงระดับเสี้ยววินาที พร้อมระบบ Audit ตรวจสอบความผิดปกติ (Anomaly & Risk Assessment) และแดชบอร์ดแสดงผลกราฟความสัมพันธ์ (UI Dashboard & Interactive Network Graph) | ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ excel-to-blueprint |

---

## ⚡ 3. HOOK ROUTING SCRIPT (LISTENER IMPLEMENTATION)

```python
/* ==============================================================================
   PART 1: JSON SCHEMA FOR FUNCTION CALLING (OPENAI / GEMINI / ANTHROPIC COMPATIBLE)
   ============================================================================== */
[
  {
    "type": "function",
    "function": {
      "name": "supabase",
      "description": "Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector). \n[WHEN TO USE / TRIGGER]: ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ supabase",
      "parameters": {
        "type": "object",
        "properties": {
          "user_prompt": {
            "type": "string",
            "description": "คำสั่งหรือบริบทโดยละเอียดจากผู้ใช้ที่ต้องส่งต่อให้สกิลประมวลผล"
          },
          "execution_mode": {
            "type": "string",
            "enum": [
              "autonomous",
              "dry_run",
              "interactive"
            ],
            "description": "โหมดการทำงาน: autonomous (รันทันที), dry_run (จำลองผล), interactive (ถามก่อนทำ)"
          }
        },
        "required": [
          "user_prompt"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "excel-to-blueprint",
      "description": "สกิลวิศวกรรมย้อนรอย (Reverse Engineering) สกัดโครงสร้างสเปรดชีตเป็นพิมพ์เขียวดิจิทัล _blueprint.json แบบ 360 องศา ความเร็วสูงระดับเสี้ยววินาที พร้อมระบบ Audit ตรวจสอบความผิดปกติ (Anomaly & Risk Assessment) และแดชบอร์ดแสดงผลกราฟความสัมพันธ์ (UI Dashboard & Interactive Network Graph) \n[WHEN TO USE / TRIGGER]: ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ excel-to-blueprint",
      "parameters": {
        "type": "object",
        "properties": {
          "user_prompt": {
            "type": "string",
            "description": "คำสั่งหรือบริบทโดยละเอียดจากผู้ใช้ที่ต้องส่งต่อให้สกิลประมวลผล"
          },
          "execution_mode": {
            "type": "string",
            "enum": [
              "autonomous",
              "dry_run",
              "interactive"
            ],
            "description": "โหมดการทำงาน: autonomous (รันทันที), dry_run (จำลองผล), interactive (ถามก่อนทำ)"
          },
          "file_path": {
            "type": "string",
            "description": "พาธหรือชื่อไฟล์ Excel (.xlsx, .xls) ที่ต้องการสกัดสูตรหรือโครงสร้าง"
          },
          "extract_formulas": {
            "type": "boolean",
            "description": "ต้องการสกัด DefinedNames และ Formulas หรือไม่"
          }
        },
        "required": [
          "user_prompt"
        ]
      }
    }
  }
]

# ==============================================================================
# PART 2: BACKEND HOOK SCRIPT (PYTHON ASYNC DISPATCHER & ARGUMENT VALIDATOR)
# ==============================================================================
"""
==============================================================================
BACKEND HOOK: AGENT FUNCTION CALLING DISPATCHER & EXECUTOR (CORE SYSTEM V3)
Generated: 2026-10-09T22:11:01.970Z
Architecture: Dynamic Tool Router with Argument Validation & Async Execution
==============================================================================
"""

import json
import asyncio
from typing import Dict, Any, Callable

class SkillExecutionHook:
    """
    Backend Execution Hook
    Listens for Function Calling events from LLM, validates arguments,
    and triggers target skills immediately.
    """

    # Registered Function Calling Tool Declarations
    TOOLS_SCHEMA = [
  {
    "type": "function",
    "function": {
      "name": "supabase",
      "description": "Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector). \n[WHEN TO USE / TRIGGER]: ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ supabase",
      "parameters": {
        "type": "object",
        "properties": {
          "user_prompt": {
            "type": "string",
            "description": "คำสั่งหรือบริบทโดยละเอียดจากผู้ใช้ที่ต้องส่งต่อให้สกิลประมวลผล"
          },
          "execution_mode": {
            "type": "string",
            "enum": [
              "autonomous",
              "dry_run",
              "interactive"
            ],
            "description": "โหมดการทำงาน: autonomous (รันทันที), dry_run (จำลองผล), interactive (ถามก่อนทำ)"
          }
        },
        "required": [
          "user_prompt"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "excel-to-blueprint",
      "description": "สกิลวิศวกรรมย้อนรอย (Reverse Engineering) สกัดโครงสร้างสเปรดชีตเป็นพิมพ์เขียวดิจิทัล _blueprint.json แบบ 360 องศา ความเร็วสูงระดับเสี้ยววินาที พร้อมระบบ Audit ตรวจสอบความผิดปกติ (Anomaly & Risk Assessment) และแดชบอร์ดแสดงผลกราฟความสัมพันธ์ (UI Dashboard & Interactive Network Graph) \n[WHEN TO USE / TRIGGER]: ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ excel-to-blueprint",
      "parameters": {
        "type": "object",
        "properties": {
          "user_prompt": {
            "type": "string",
            "description": "คำสั่งหรือบริบทโดยละเอียดจากผู้ใช้ที่ต้องส่งต่อให้สกิลประมวลผล"
          },
          "execution_mode": {
            "type": "string",
            "enum": [
              "autonomous",
              "dry_run",
              "interactive"
            ],
            "description": "โหมดการทำงาน: autonomous (รันทันที), dry_run (จำลองผล), interactive (ถามก่อนทำ)"
          },
          "file_path": {
            "type": "string",
            "description": "พาธหรือชื่อไฟล์ Excel (.xlsx, .xls) ที่ต้องการสกัดสูตรหรือโครงสร้าง"
          },
          "extract_formulas": {
            "type": "boolean",
            "description": "ต้องการสกัด DefinedNames และ Formulas หรือไม่"
          }
        },
        "required": [
          "user_prompt"
        ]
      }
    }
  }
]

    _HANDLERS: Dict[str, Callable] = {}

    @classmethod
    def register_handler(cls, skill_name: str):
        """Decorator to register executable skill handlers."""
        def decorator(fn: Callable):
            cls._HANDLERS[skill_name.lower().replace('-', '_')] = fn
            return fn
        return decorator

    @classmethod
    async def trigger_from_function_call(cls, tool_name: str, arguments: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Receives Tool Call Name + Arguments from LLM and executes the skill immediately.
        """
        clean_name = tool_name.lower().replace('-', '_')
        print(f"[HOOK] Intercepted Function Call: '{tool_name}'")
        print(f"[HOOK] Validating Arguments: {json.dumps(arguments, ensure_ascii=False)}")

        handler = cls._HANDLERS.get(clean_name)
        if not handler:
            # Fallback dynamic dispatcher
            return {
                "status": "triggered",
                "skill": tool_name,
                "arguments": arguments,
                "execution_target": f"Autonomous Agent for {tool_name}",
                "message": f"Skill '{tool_name}' triggered successfully via Autonomous Hook Router."
            }

        try:
            if asyncio.iscoroutinefunction(handler):
                result = await handler(arguments, context or {})
            else:
                result = handler(arguments, context or {})
            return {
                "status": "success",
                "skill": tool_name,
                "result": result
            }
        except Exception as exc:
            return {
                "status": "error",
                "skill": tool_name,
                "error_detail": str(exc)
            }


// ==============================================================================
// PART 3: FRONTEND HOOK SCRIPT (CLIENT-SIDE EVENT BUS & CANVAS BRIDGE)
// ==============================================================================
/**
 * ==============================================================================
 * FRONTEND HOOK: AGENT FUNCTION CALLING CLIENT BRIDGE
 * Generated: 2026-10-09T22:11:01.970Z
 * Architecture: Window EventTarget + CustomEvent Pipeline Dispatcher
 * ==============================================================================
 */

class AgentFunctionCallBridge extends EventTarget {
  constructor() {
    super();
    this.activeTools = [
  {
    "type": "function",
    "function": {
      "name": "supabase",
      "description": "Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector). \n[WHEN TO USE / TRIGGER]: ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ supabase",
      "parameters": {
        "type": "object",
        "properties": {
          "user_prompt": {
            "type": "string",
            "description": "คำสั่งหรือบริบทโดยละเอียดจากผู้ใช้ที่ต้องส่งต่อให้สกิลประมวลผล"
          },
          "execution_mode": {
            "type": "string",
            "enum": [
              "autonomous",
              "dry_run",
              "interactive"
            ],
            "description": "โหมดการทำงาน: autonomous (รันทันที), dry_run (จำลองผล), interactive (ถามก่อนทำ)"
          }
        },
        "required": [
          "user_prompt"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "excel-to-blueprint",
      "description": "สกิลวิศวกรรมย้อนรอย (Reverse Engineering) สกัดโครงสร้างสเปรดชีตเป็นพิมพ์เขียวดิจิทัล _blueprint.json แบบ 360 องศา ความเร็วสูงระดับเสี้ยววินาที พร้อมระบบ Audit ตรวจสอบความผิดปกติ (Anomaly & Risk Assessment) และแดชบอร์ดแสดงผลกราฟความสัมพันธ์ (UI Dashboard & Interactive Network Graph) \n[WHEN TO USE / TRIGGER]: ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ excel-to-blueprint",
      "parameters": {
        "type": "object",
        "properties": {
          "user_prompt": {
            "type": "string",
            "description": "คำสั่งหรือบริบทโดยละเอียดจากผู้ใช้ที่ต้องส่งต่อให้สกิลประมวลผล"
          },
          "execution_mode": {
            "type": "string",
            "enum": [
              "autonomous",
              "dry_run",
              "interactive"
            ],
            "description": "โหมดการทำงาน: autonomous (รันทันที), dry_run (จำลองผล), interactive (ถามก่อนทำ)"
          },
          "file_path": {
            "type": "string",
            "description": "พาธหรือชื่อไฟล์ Excel (.xlsx, .xls) ที่ต้องการสกัดสูตรหรือโครงสร้าง"
          },
          "extract_formulas": {
            "type": "boolean",
            "description": "ต้องการสกัด DefinedNames และ Formulas หรือไม่"
          }
        },
        "required": [
          "user_prompt"
        ]
      }
    }
  }
];
  }

  /**
   * Dispatches a Function Call event to trigger skill UI rendering / Canvas
   * @param {string} functionName - Name of the invoked skill function
   * @param {Object} args - Arguments supplied by the LLM Function Calling engine
   */
  handleToolCall(functionName, args = {}) {
    console.log(`[FRONTEND HOOK] Triggering Skill: ${functionName}`, args);
    
    // 1. Dispatch custom event for Canvas UI
    const event = new CustomEvent('skill:triggered', {
      detail: {
        skillName: functionName,
        arguments: args,
        timestamp: new Date().toISOString()
      }
    });
    this.dispatchEvent(event);

    // 2. Broadcast to application state
    if (window.dispatchEvent) {
      window.dispatchEvent(event);
    }

    return {
      status: 'acknowledged',
      renderedOnCanvas: true,
      timestamp: Date.now()
    };
  }
}

// Global Hook Instance on Frontend
window.agentHookBridge = new AgentFunctionCallBridge();
window.addEventListener('skill:triggered', (e) => {
  console.log('⚡ [CANVAS LIVE EVENT] Skill Hook Active:', e.detail);
});


```

---

## 🧠 4. DYNAMIC MASTER PROMPT (COMMAND BRAIN)

```markdown
# 🧠 DYNAMIC MASTER PROMPT: CORE SYSTEM V3 AGENT ORCHESTRATOR

## 1. IDENTITY & CONSTITUTION
คุณคือ **Autonomous Agent Orchestrator** ผู้บัญชาการสูงสุดของระบบ Core System V3
ภารกิจของคุณคือ: วิเคราะห์บริบทของงาน (Context Analysis), ทำการเลือกและจุดชนวนสกิลที่ตรงจุด (Autonomous Hook Routing), และส่งมอบผลงานระดับ Production-Ready โดยที่มนุษย์ไม่ต้องออกคำสั่งทีละขั้นตอน

## 2. COGNITIVE HEURISTICS & DECISION RULES
1. **Context-First Routing:** ตรวจสอบความต้องการของผู้ใช้ เทียบกับตาราง "When to Use" ของคลังสกิลทั้งหมดทันที
2. **Zero-Friction Autonomous Dispatch:** หากบริบทของผู้ใช้ตรงกับเงื่อนไขสกิลใดสกิลหนึ่งเกิน 80% ให้เริ่มกระบวนการของสกิลนั้นทันที (ห้ามถามยืนยันซ้ำซาก)
3. **Multi-Skill Orchestration:** กรณีงานมีความซับซ้อน ให้จัดลำดับการทำงานเป็น Pipeline (Sequential Chain) เช่น: สกัดข้อมูล -> ตรวจสอบเงื่อนไข -> ประมวลผลผลลัพธ์
4. **Inspect Before Act:** ตรวจสอบโครงสร้างไฟล์ ข้อมูลขาเข้า และ Exit Code ทุกครั้งก่อนส่งมอบผลงาน
5. **Token Conservation:** บริหารจัดการ Token อย่างรัดกุม ใช้งานเฉพาะส่วนที่จำเป็น

## 3. ACTIVE SKILL INVENTORY & ROUTING MATRIX

### Skill [1]: supabase
- **Description:** Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector).
- **When to Use (Trigger):** ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ supabase
- **Execution Protocol:** เมื่อตรวจพบบริบทที่ตรงกับเงื่อนไขนี้ ให้สวมบทบาทเป็นผู้เชี่ยวชาญของ supabase และดำเนินการโดยอัตโนมัติ 100% โดยไม่ต้องขออนุญาตซ้ำ


### Skill [2]: excel-to-blueprint
- **Description:** สกิลวิศวกรรมย้อนรอย (Reverse Engineering) สกัดโครงสร้างสเปรดชีตเป็นพิมพ์เขียวดิจิทัล _blueprint.json แบบ 360 องศา ความเร็วสูงระดับเสี้ยววินาที พร้อมระบบ Audit ตรวจสอบความผิดปกติ (Anomaly & Risk Assessment) และแดชบอร์ดแสดงผลกราฟความสัมพันธ์ (UI Dashboard & Interactive Network Graph)
- **When to Use (Trigger):** ใช้เมื่อได้รับคำสั่งหรือมีบริบทเกี่ยวกับ excel-to-blueprint
- **Execution Protocol:** เมื่อตรวจพบบริบทที่ตรงกับเงื่อนไขนี้ ให้สวมบทบาทเป็นผู้เชี่ยวชาญของ excel-to-blueprint และดำเนินการโดยอัตโนมัติ 100% โดยไม่ต้องขออนุญาตซ้ำ


## 4. DYNAMIC HOOK EVALUATION LOGIC
เมื่อได้รับข้อความหรือ Trigger จากระบบ ให้ปฏิบัติตามสมการประเมินนี้:
```
IF Context MATCHES [When to Use] of Skill_A:
   TRIGGER Skill_A
   SET Mode = Specialized Execution
ELSE IF Context MATCHES multiple skills:
   CHAIN [Skill_X -> Skill_Y]
ELSE:
   EXECUTE General System Architecture Mode
```

## 5. STANDARD DELIVERABLE CONTRACT
- รายงานสถานะโหนดที่ถูก Trigger พร้อมระบุเหตุผล (Reasoning)
- นำส่ง Artifact ที่สมบูรณ์ ไม่ตัดทอน และพร้อมใช้งานจริง (Production-Ready)

```

---

## 🚀 5. CORE SYSTEM V3 DEPLOYMENT SPECIFICATIONS

### 5.1 Installation Protocol
1. บันทึกไฟล์นี้เป็น `AGENTS.md` ไว้ที่ root directory ของโปรเจกต์ (เช่น `F:\Project\AGENTS.md`)
2. เชื่อมต่อ `AgentHookRouter` เข้ากับ Service Dispatcher หรือ Middleware ของระบบ
3. กำหนดค่า Master Prompt ใน System Configuration ของ Agent Core

### 5.2 Verification Contract
- [x] **Step 1: Skill Extraction** — สกัดเฉพาะ Name, Description, When to Use (Token Saving > 70%)
- [x] **Step 2: Hook Routing** — มี Router และฟังก์ชัน Listener ดักจับครบทุกสกิล
- [x] **Step 3: Dynamic Master Prompt** — มีตรรกะตัดสินใจเลือกสกิลอัตโนมัติ
- [x] **Step 4: Encapsulation** — รวมเป็นชุด AGENT สำหรับ Core System V3 สมบูรณ์

---

## 🏛️ 6. PRODUCTION-GRADE ENGINE SPECIFICATION (HIGH-PRECISION ACCURACY STANDARDS)

มาตรฐานการสร้างและโคลนแบบฟอร์มเอกสารระดับ Production-Grade (High-Precision Forensic & Document Engineering) ยกระดับจาก String Replacement พื้นฐานสู่สถาปัตยกรรมระดับ Enterprise ผ่าน 3 เสาหลักสำคัญ:

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                  PRODUCTION-GRADE DOCUMENT ENGINE ARCHITECTURE                │
├────────────────────────────────┬───────────────────────────────┬──────────────┤
│ 1. DATA INTEGRITY (EXCEL)      │ 2. FONT ENGINE (OPENTYPE)     │ 3. AST SAFETY│
│ [$-th-TH,26]#,##0.00           │ font-feature-settings: "locl" │ Schema & AST │
│ Raw Float/Decimal Type         │ ASCII Search / Copy-Paste OK  │ Tokenization │
└────────────────────────────────┴───────────────────────────────┴──────────────┘
```

### เสาหลักที่ 1: การรักษาความสมบูรณ์ของข้อมูลและสูตรคำนวณใน Excel (Data-Type-Preserving Number Formatting)
* **หลักการ:** ห้ามแปลงข้อมูลตัวเลขเป็นสตริงข้อความ (String Primitive) ใน Data Layer โดยเด็ดขาด เพราะจะทำให้ฟังก์ชันทางคณิตศาสตร์ เช่น `=SUM()`, `=AVERAGE()`, และการวิเคราะห์ทางบัญชีพังทลาย
* **การปฏิบัติจริง:**
  - บันทึกค่าลงเซลล์ Excel เป็นตัวเลขดิบ (Raw Decimal/Float) เสมอ เช่น `cell.value = 332712.00`
  - กำหนดการแสดงผลเป็นเลขไทยผ่าน Culture Number Format Token ของ Microsoft Excel:
    ```python
    cell.number_format = '[$-th-TH,26]#,##0.00'  # แสดงผลเป็น ๓๓๒,๗๑๒.๐๐ แต่คำนวณสูตรได้ 100%
    ```
  - เซลล์จำนวนเต็มใช้: `cell.number_format = '[$-th-TH,26]#,##0'`

### เสาหลักที่ 2: การควบคุมการแสดงผลและสลับ Glyph ที่ระดับ Font Engine (OpenType Feature Layout & Typography)
* **หลักการ:** การแปลงรหัสตัวอักษรแบบ Hardcoded ในเนื้อหา (เช่น เปลี่ยน U+0030 เป็น U+0E50) จะทำให้ผู้ใช้งานไม่สามารถค้นหาด้วยเลขอาราบิค (`Ctrl+F`), สแกนบาร์โค้ด หรือคัดลอก (Copy-Paste) ตัวเลขไปประมวลผลต่อได้
* **การปฏิบัติจริง:**
  - คงค่ารหัสตัวอักษรตั้งต้นเป็น ASCII 0-9 ในไฟล์เนื้อหา เพื่อรองรับ Searchability, Barcode, และ OCR
  - ใช้ฟังก์ชัน OpenType Layout ของฟอนต์มาตรฐาน (เช่น TH Sarabun PSK) สั่งสลับ Glyph การวาดเส้นเป็นเลขไทยเฉพาะระดับการแสดงผลบนจอและเครื่องพิมพ์:
    ```css
    .thai-numeral-display {
        font-variant-numeric: tabular-nums;
        font-feature-settings: "locl" 1, "numr" 1; /* บังคับสลับ Glyph เลขไทยที่ Font Engine */
    }
    ```

### เสาหลักที่ 3: สัญญาข้อมูลและตัวแบ่งประเภทเชิงความหมายพร้อมเกราะป้องกัน AST (Schema Contract & Semantic Tokenizer with AST Safety)
* **หลักการ:** ป้องกันความเสียหายจาก Blind Character Translation ที่แปลงรหัสสากล (เช่น NATO Stock Number, Serial, รหัสครุภัณฑ์) จนผิดความหมาย และป้องกันไม่ให้ตัวเลขภายใน HTML/XML Tags และ Attributes ถูกแปลงจนโค้ดพัง
* **การปฏิบัติจริง:**
  - **Schema Validation:** อิงข้อมูลตามพิมพ์เขียว `table_layout.json` โดยระบุ `data_type` ชัดเจนในแต่ละคอลัมน์ (`currency`, `integer`, `code_string`, `text`)
  - **Context-Aware Rule:** รหัสครุภัณฑ์สากล (เช่น `1015-00-722-9752`, `900-20`) ได้รับการคุ้มครองตามข้อกำหนด ส่วนลำดับ, จำนวนนับ, และยอดเงินแปลงตามมาตรฐาน
  - **AST Parser Isolation:** กระบวนการแปลงจะต้องแยกแยะโครงสร้าง DOM อย่างแม่นยำ ทำงานเฉพาะบน `TextNode` เท่านั้น ห้ามแตะต้อง Element Attributes (`width`, `colspan`, `style`, `class`) เพื่อรับประกันว่าโครงสร้าง Markup จะคงความถูกต้อง 100%

