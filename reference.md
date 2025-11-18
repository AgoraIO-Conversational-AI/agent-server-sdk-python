# Reference
## Agent Management
<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">start</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create and start a Conversational AI agent instance.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora
from agoraio.agent_management import (
    AgentManagementStartRequestProperties,
    AgentManagementStartRequestPropertiesAdvancedFeatures,
    AgentManagementStartRequestPropertiesAsr,
    AgentManagementStartRequestPropertiesLlm,
    AgentManagementStartRequestPropertiesTts,
)

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.start(
    appid="appid",
    name="unique_name",
    properties=AgentManagementStartRequestProperties(
        channel="channel_name",
        token="token",
        agent_rtc_uid="1001",
        remote_rtc_uids=["1002"],
        idle_timeout=120,
        advanced_features=AgentManagementStartRequestPropertiesAdvancedFeatures(
            enable_aivad=True,
        ),
        asr=AgentManagementStartRequestPropertiesAsr(
            language="en-US",
        ),
        tts=AgentManagementStartRequestPropertiesTts(
            vendor="microsoft",
            params={
                "key": "<your_tts_api_key>",
                "region": "eastus",
                "voice_name": "en-US-AndrewMultilingualNeural",
            },
        ),
        llm=AgentManagementStartRequestPropertiesLlm(
            url="https://api.openai.com/v1/chat/completions",
            api_key="<your_llm_key>",
            system_messages=[
                {"role": "system", "content": "You are a helpful chatbot."}
            ],
            params={"model": "gpt-4o-mini"},
            max_history=32,
            greeting_message="Hello, how can I assist you today?",
            failure_message="Please hold on a second.",
        ),
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The unique identifier of the agent. The same identifier cannot be used repeatedly.
    
</dd>
</dl>

<dl>
<dd>

**properties:** `AgentManagementStartRequestProperties` — Configuration details of the agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a list of agents that meet the specified conditions.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
response = client.agent_management.list(
    appid="appid",
    channel="channel",
    from_time=1.1,
    to_time=1.1,
    state="0",
    limit=1,
    cursor="cursor",
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**channel:** `typing.Optional[str]` — The channel to query for a list of agents.
    
</dd>
</dl>

<dl>
<dd>

**from_time:** `typing.Optional[float]` — The start timestamp (in seconds) for the query. Default is 2 hours ago.
    
</dd>
</dl>

<dl>
<dd>

**to_time:** `typing.Optional[float]` — The end timestamp (in seconds) for the query. Default is current time.
    
</dd>
</dl>

<dl>
<dd>

**state:** `typing.Optional[AgentManagementListRequestState]` 

The agent state to filter by. Only one state can be specified per query:
- `IDLE` (0): Agent is idle.
- `STARTING` (1): The agent is being started.
- `RUNNING` (2): The agent is running.
- `STOPPING` (3): The agent is stopping.
- `STOPPED` (4): The agent has exited.
- `RECOVERING` (5): The agent is recovering.
- `FAILED` (6): The agent failed to execute.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The maximum number of entries returned per page.
    
</dd>
</dl>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — The paging cursor, indicating the starting position (`agent_id`) of the next page of results.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the current state information of the specified agent instance.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.get(
    appid="appid",
    agent_id="agentId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent instance ID you obtained after successfully calling `join` to start a conversational AI agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">get_history</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get the history of the conversation between the user and the agent.

Call this endpoint while the agent is running to retrieve the conversation history. You can set the maximum number of cached entries using the `llm.max_history` parameter when calling the start agent endpoint. The default value is `32`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.get_history(
    appid="appid",
    agent_id="agentId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent instance ID you obtained after successfully calling `join` to start a conversational AI agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">stop</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Stop the specified conversational agent instance.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.stop(
    appid="appid",
    agent_id="agentId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent instance ID you obtained after successfully calling `join` to start a conversational AI agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Adjust Conversation AI Engine parameters at runtime.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora
from agoraio.agent_management import (
    AgentManagementUpdateRequestProperties,
    AgentManagementUpdateRequestPropertiesLlm,
)

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.update(
    appid="appid",
    agent_id="agentId",
    properties=AgentManagementUpdateRequestProperties(
        token="007eJxTYxxxxxxxxxxIaHMLAAAA0ex66",
        llm=AgentManagementUpdateRequestPropertiesLlm(
            system_messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. xxx",
                },
                {
                    "role": "system",
                    "content": "Previously, user has talked about their favorite hobbies with some key topics: xxx",
                },
            ],
            params={"model": "abab6.5s-chat", "max_token": 1024},
        ),
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent instance ID you obtained after successfully calling `join` to start a conversational AI agent.
    
</dd>
</dl>

<dl>
<dd>

**properties:** `typing.Optional[AgentManagementUpdateRequestProperties]` — Configuration properties to update.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">speak</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Broadcast a custom message using the TTS module.

During a conversation with an agent, call this endpoint to immediately broadcast a custom message using the TTS module. Upon receiving the request, the system interrupts the agent's speech and thought process to deliver the message. This broadcast can be interrupted by human voice.

Note: The speak API is not supported when using `mllm` configuration.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.speak(
    appid="appid",
    agent_id="agentId",
    text="Sorry, the conversation content is not compliant.",
    priority="INTERRUPT",
    interruptable=False,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent instance ID you obtained after successfully calling `join` to start a conversational AI agent.
    
</dd>
</dl>

<dl>
<dd>

**text:** `str` — The broadcast message text. The maximum length of the text content is 512 bytes.
    
</dd>
</dl>

<dl>
<dd>

**priority:** `typing.Optional[AgentManagementSpeakRequestPriority]` 

Sets the priority of the message broadcast:
- `INTERRUPT`: High priority. The agent immediately interrupts the current interaction to announce the message.
- `APPEND`: Medium priority. The agent announces the message after the current interaction ends.
- `IGNORE`: Low priority. If the agent is busy interacting, it ignores and discards the broadcast; the message is only announced if the agent is not interacting.
    
</dd>
</dl>

<dl>
<dd>

**interruptable:** `typing.Optional[bool]` 

Whether to allow users to interrupt the agent's broadcast by speaking:
- `true`: Allow
- `false`: Don't allow
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agent_management.<a href="src/agoraio/agent_management/client.py">interrupt</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Interrupt the specified agent while speaking or thinking.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.agent_management.interrupt(
    appid="appid",
    agent_id="agentId",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent instance ID you obtained after successfully calling `join` to start a conversational AI agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Telephony
<details><summary><code>client.telephony.<a href="src/agoraio/telephony/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Query historical call records for a specified appid based on the filter criteria.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
response = client.telephony.list(
    appid="appid",
    number="number",
    from_time=1,
    to_time=1,
    type="inbound",
    limit=1,
    cursor="cursor",
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**number:** `typing.Optional[str]` — Filter by phone number. Can be either the calling number or the called number.
    
</dd>
</dl>

<dl>
<dd>

**from_time:** `typing.Optional[int]` — Query list start timestamp (in seconds). Default is 60 days ago.
    
</dd>
</dl>

<dl>
<dd>

**to_time:** `typing.Optional[int]` — Query list end timestamp (in seconds). Default is current time.
    
</dd>
</dl>

<dl>
<dd>

**type:** `typing.Optional[TelephonyListRequestType]` 

Call type filter:
- `inbound`: Inbound call.
- `outbound`: Outbound call.

If not specified, all call types are returned.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — Maximum number of items returned in a single page.
    
</dd>
</dl>

<dl>
<dd>

**cursor:** `typing.Optional[str]` — Pagination cursor. Use the `agent_id` from the previous page as the cursor for the next page.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.telephony.<a href="src/agoraio/telephony/client.py">call</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Initiate an outbound call to a specified number and create an agent to join the specified RTC channel.

Use this endpoint to initiate an outbound call to the specified number and create an agent that joins the target RTC channel. The agent waits for the callee to answer.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora
from agoraio.telephony import (
    TelephonyCallRequestProperties,
    TelephonyCallRequestSip,
)

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.telephony.call(
    appid="appid",
    name="customer_service",
    sip=TelephonyCallRequestSip(
        to_number="+19876543210",
        from_number="+11234567890",
        sip_rtc_uid="100",
        sip_rtc_token="<agora_sip_rtc_token>",
    ),
    properties=TelephonyCallRequestProperties(
        channel="<agora_channel>",
        token="<agora_channel_token>",
        agent_rtc_uid="111",
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name identifier of the call session.
    
</dd>
</dl>

<dl>
<dd>

**sip:** `TelephonyCallRequestSip` — SIP (Session Initiation Protocol) call configuration object.
    
</dd>
</dl>

<dl>
<dd>

**properties:** `TelephonyCallRequestProperties` 

Call attribute configuration. The content of this field varies depending on the invocation method:
- **Using pipeline ID**: Simply pass in `channel`, `token`, and `agent_rtc_uid`.
- **Using complete configuration**: Pass in the complete parameters of the [Start a conversational AI agent](https://docs.agora.io/en/conversational-ai/rest-api/agent/join) `properties`, including all required fields such as `channel`, `token`, `agent_rtc_uid`, `remote_rtc_uids`, `tts`, and `llm`.
    
</dd>
</dl>

<dl>
<dd>

**pipeline_id:** `typing.Optional[str]` — The unique ID of a published project in AI Studio.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.telephony.<a href="src/agoraio/telephony/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve the call status and related information of a specified agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.telephony.get(
    appid="appid",
    agent_id="agent_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent ID you obtained after successfully calling the API to initiate an outbound call.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.telephony.<a href="src/agoraio/telephony/client.py">hangup</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Instruct the agent to proactively hang up the ongoing call and leave the RTC channel.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.telephony.hangup(
    appid="appid",
    agent_id="agent_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**appid:** `str` — The App ID of the project.
    
</dd>
</dl>

<dl>
<dd>

**agent_id:** `str` — The agent ID you obtained after successfully calling the API to initiate an outbound call.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Phone Number Management
<details><summary><code>client.phone_number_management.<a href="src/agoraio/phone_number_management/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a list of all imported phone numbers under the current account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.phone_number_management.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.phone_number_management.<a href="src/agoraio/phone_number_management/client.py">add</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Import a pre-configured phone number that can be used for inbound or outbound calls.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora
from agoraio.phone_number_management import (
    PhoneNumberManagementAddRequestInboundConfig,
    PhoneNumberManagementAddRequestOutboundConfig,
)

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.phone_number_management.add(
    provider="byo",
    phone_number="+19876543210",
    label="Sales Hotline",
    inbound=True,
    outbound=True,
    inbound_config=PhoneNumberManagementAddRequestInboundConfig(
        allowed_addresses=["112.126.15.64/27"],
    ),
    outbound_config=PhoneNumberManagementAddRequestOutboundConfig(
        address="xxx:xxx@sip.example.com",
        transport="tls",
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**provider:** `PhoneNumberManagementAddRequestProvider` 

Number provider:
- `byo`: BYO (Bring Your Own)
- `twilio`: Twilio
    
</dd>
</dl>

<dl>
<dd>

**phone_number:** `str` — Telephone number in E.164 format.
    
</dd>
</dl>

<dl>
<dd>

**label:** `str` — A label used to identify the number.
    
</dd>
</dl>

<dl>
<dd>

**inbound_config:** `PhoneNumberManagementAddRequestInboundConfig` — SIP inbound call configuration.
    
</dd>
</dl>

<dl>
<dd>

**outbound_config:** `PhoneNumberManagementAddRequestOutboundConfig` — SIP outbound call configuration.
    
</dd>
</dl>

<dl>
<dd>

**inbound:** `typing.Optional[bool]` — Whether the number supports inbound calls.
    
</dd>
</dl>

<dl>
<dd>

**outbound:** `typing.Optional[bool]` — Whether the number supports outbound calls.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.phone_number_management.<a href="src/agoraio/phone_number_management/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve detailed information for a specific phone number.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.phone_number_management.get(
    phone_number="phone_number",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number:** `str` — Telephone number in E.164 format. For example, +11234567890.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.phone_number_management.<a href="src/agoraio/phone_number_management/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Remove an imported phone number from the system.

Note: This operation only removes the number configuration from the Agora system; the number stored with the phone service provider is not deleted. After calling this endpoint, the number stops receiving calls routed through this system. To delete the number from the service provider, remove it in the service provider's console.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.phone_number_management.delete(
    phone_number="phone_number",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number:** `str` — Telephone number in E.164 format. For example, +11234567890.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.phone_number_management.<a href="src/agoraio/phone_number_management/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update the configuration for a phone number.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from agoraio import Agora
from agoraio.phone_number_management import (
    PhoneNumberManagementUpdateRequestInboundConfig,
    PhoneNumberManagementUpdateRequestOutboundConfig,
)

client = Agora(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
)
client.phone_number_management.update(
    phone_number="phone_number",
    inbound_config=PhoneNumberManagementUpdateRequestInboundConfig(
        pipeline_id="xxxxx",
    ),
    outbound_config=PhoneNumberManagementUpdateRequestOutboundConfig(
        pipeline_id="xxxxx",
    ),
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**phone_number:** `str` — Telephone number in E.164 format. For example, +11234567890.
    
</dd>
</dl>

<dl>
<dd>

**inbound_config:** `typing.Optional[PhoneNumberManagementUpdateRequestInboundConfig]` — Update inbound call configuration. Passing `null` will clear the configuration.
    
</dd>
</dl>

<dl>
<dd>

**outbound_config:** `typing.Optional[PhoneNumberManagementUpdateRequestOutboundConfig]` — Update outbound call configuration. Passing `null` will clear the configuration.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

